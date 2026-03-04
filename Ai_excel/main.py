from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import time
from pathlib import Path
import shutil
import tempfile

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# simple in-memory cache: filename -> { 'mtime': float, 'xls': dict(sheet_name->DataFrame) }
CACHE = {}

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    files = [f.name for f in UPLOAD_DIR.glob("*") if f.is_file()]
    return templates.TemplateResponse("index.html", {"request": request, "files": files})


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    dest = UPLOAD_DIR / file.filename
    with dest.open("wb") as f:
        shutil.copyfileobj(file.file, f)
    # invalidate cache for this file
    if file.filename in CACHE:
        del CACHE[file.filename]
    return {"filename": file.filename}


@app.get("/files")
async def list_files():
    files = [f.name for f in UPLOAD_DIR.glob("*") if f.is_file()]
    return {"files": files}


@app.post("/search")
async def search(filename: str = Form(...), keyword: str = Form(...), sheet: str = Form(None), page: int = Form(1), page_size: int = Form(50)):
    path = UPLOAD_DIR / filename
    if not path.exists():
        return JSONResponse({"error": "file not found"}, status_code=404)
    # load with cache if file unchanged
    try:
        mtime = path.stat().st_mtime
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
    if filename in CACHE and CACHE[filename]["mtime"] == mtime:
        xls = CACHE[filename]["xls"]
    else:
        try:
            xls = pd.read_excel(path, sheet_name=None, engine="openpyxl", dtype=str)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        CACHE[filename] = {"mtime": mtime, "xls": xls}

    result = []
    target_sheets = [sheet] if sheet else list(xls.keys())
    for sheet_name in target_sheets:
        if sheet_name not in xls:
            continue
        df = xls[sheet_name]
        if df is None or df.empty:
            continue
        # faster matching: aggregate row into single string column then vectorized contains
        df_filled = df.fillna("")
        if keyword.strip() == "":
            # no keyword -> no match
            continue
        # aggregate values per row into single string to reduce repeated regex work
        try:
            combined = df_filled.astype(str).agg(' '.join, axis=1)
        except Exception:
            # fallback
            combined = df_filled.apply(lambda row: ' '.join(row.astype(str)), axis=1)
        mask = combined.str.contains(keyword, case=False, na=False)
        matched = df_filled[mask]
        total = int(matched.shape[0])
        if total == 0:
            continue
        if page_size <= 0:
            page_size = 50
        start = (page - 1) * page_size
        end = start + page_size
        page_rows = matched.iloc[start:end]
        header = [str(c) for c in df.columns.tolist()]
        rows = []
        for idx, row in page_rows.iterrows():
            rows.append({"row_index": int(idx), "values": [str(v) for v in row.tolist()]})
        result.append({"sheet": sheet_name, "header": header, "rows": rows, "total": total, "page": page, "page_size": page_size})
    return {"result": result}


@app.post("/export")
async def export(filename: str = Form(...)):
    """Return the original uploaded Excel file for download (entire workbook)."""
    path = UPLOAD_DIR / filename
    if not path.exists():
        return JSONResponse({"error": "file not found"}, status_code=404)
    try:
        return FileResponse(path, filename=filename, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.post("/save_changes")
async def save_changes(payload: dict):
    # payload: {filename, sheet, action: update/add/delete, row_index, values}
    try:
        filename = payload["filename"]
        sheet = payload["sheet"]
        action = payload.get("action")
    except Exception:
        return JSONResponse({"error": "invalid payload"}, status_code=400)
    path = UPLOAD_DIR / filename
    if not path.exists():
        return JSONResponse({"error": "file not found"}, status_code=404)
    try:
        xls = pd.read_excel(path, sheet_name=None, engine="openpyxl", dtype=str)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
    if sheet not in xls:
        return JSONResponse({"error": "sheet not found"}, status_code=404)
    df = xls[sheet].fillna("")
    if action == "update":
        row_index = int(payload["row_index"])
        values = payload["values"]
        for i, col in enumerate(df.columns):
            df.at[row_index, col] = values[i] if i < len(values) else ""
        xls[sheet] = df
    elif action == "delete":
        row_index = int(payload["row_index"])
        df = df.drop(df.index[row_index]).reset_index(drop=True)
        xls[sheet] = df
    elif action == "add":
        values = payload["values"]
        new_row = {col: (values[i] if i < len(values) else "") for i, col in enumerate(df.columns)}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        xls[sheet] = df
    else:
        return JSONResponse({"error": "unknown action"}, status_code=400)
    try:
        with pd.ExcelWriter(path, engine="openpyxl") as writer:
            for sname, s_df in xls.items():
                s_df.to_excel(writer, sheet_name=sname, index=False)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
    # invalidate cache because file changed
    if filename in CACHE:
        del CACHE[filename]
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
