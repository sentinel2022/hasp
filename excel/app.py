# -*- coding: utf-8 -*-
import os
import pandas as pd
from flask import Flask, request, redirect, url_for, render_template, send_from_directory

# --- 配置 ---
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

# 确保上传文件夹存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 限制上传文件大小为 16MB

app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  #设置在主程序所在目录查找上传文件


# --- 新增：用于存储上次上传的文件信息 ---
# 在实际应用中，你可能会使用数据库来为每个用户存储，但这里我们用一个全局变量简化
LAST_UPLOADED_FILE_PATH = None

# --- 辅助函数 (保持不变) ---
def allowed_file(filename):
    """检查文件扩展名是否合法"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def search_in_excel(filepath, keyword):
    """在 Excel 文件中搜索关键字"""
    results = []
    try:
        with pd.ExcelFile(filepath) as xls:
            for sheet_name in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=sheet_name)
                data_rows = df.values.tolist()
                if not data_rows:
                    continue
                header = df.columns.tolist()
                found_rows_in_sheet = [row for row in data_rows if any(str(keyword).lower() in str(cell).lower() for cell in row)]
                if found_rows_in_sheet:
                    results.append([f"--- 工作表: '{sheet_name}' ---"] + [''] * (len(header) - 1))
                    results.append(header)
                    results.extend(found_rows_in_sheet)
                    results.append([''] * len(header))
    except Exception as e:
        print(f"处理 Excel 文件时出错: {e}")
        results = [["错误：无法解析 Excel 文件。请确保文件格式正确。"]]
    return results

# --- 路由 ---
@app.route('/')
def index():
    """显示上传表单，并传递上次上传的文件名"""
    last_filename = os.path.makedirs(LAST_UPLOADED_FILE_PATH) if LAST_UPLOADED_FILE_PATH else None
    return render_template('index.html', last_filename=last_filename)

@app.route('/search', methods=['POST'])
def search():
    """处理文件上传和搜索请求"""
    global LAST_UPLOADED_FILE_PATH # 使用全局变量
    
    file = request.files['file']
    keyword = request.form.get('keyword', '')
    use_last_file = request.form.get('use_last_file') # 检查是否点击了“使用上次文件”
    
    # 确定要使用的文件路径
    target_filepath = None
    
    if file and file.filename != '' and allowed_file(file.filename):
        # 情况1: 用户上传了新文件
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        target_filepath = filepath
        # 更新“上次上传”的文件路径
        LAST_UPLOADED_FILE_PATH = filepath 
    elif use_last_file and LAST_UPLOADED_FILE_PATH and os.path.exists(LAST_UPLOADED_FILE_PATH):
        # 情况2: 用户点击了“使用上次文件”，并且上次的文件存在
        target_filepath = LAST_UPLOADED_FILE_PATH
    else:
        # 情况3: 既没有新文件，也没有有效的上次文件
        message = "请选择一个新文件，或确保之前已成功上传过文件。"
        return render_template('index.html', message=message, last_filename=os.path.basename(LAST_UPLOADED_FILE_PATH) if LAST_UPLOADED_FILE_PATH else None)

    # 检查关键字
    if not keyword:
        message = "请输入查询关键字。"
        # 如果是新上传的文件，需要删除它
        if file and file.filename != '':
            os.remove(target_filepath)
        return render_template('index.html', message=message, last_filename=os.path.basename(LAST_UPLOADED_FILE_PATH) if LAST_UPLOADED_FILE_PATH else None)

    # 在目标文件中搜索
    search_results = search_in_excel(target_filepath, keyword)
    
    # **注意**: 我们不再删除文件，因为我们需要保留它以供下次使用
    # os.remove(target_filepath) # 删除这行代码
    
    return render_template('results.html', 
                           keyword=keyword, 
                           results=search_results)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8090, debug=True)