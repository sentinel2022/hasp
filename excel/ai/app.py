import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
import pandas as pd
from werkzeug.utils import secure_filename
import sys

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# 配置上传文件夹
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_uploaded_files():
    """获取已上传的文件列表"""
    files = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if allowed_file(filename):
            try:
                # 尝试解码文件名（针对Python 2兼容性）
                if sys.version_info[0] < 3:
                    filename = filename.decode('utf-8')
            except:
                pass
            files.append(filename)
    return files

def secure_filename_custom(filename):
    """自定义安全文件名函数，保留中文字符"""
    # 保留中文字符、数字、字母、下划线和点
    keep_chars = (' ', '.', '_', '-')
    filename = "".join(c for c in filename if c.isalnum() or c in keep_chars).strip()
    return filename

def search_in_excel(filepath, keyword):
    """在Excel文件中搜索关键字"""
    results = []
    
    try:
        # 读取Excel文件
        xls = pd.ExcelFile(filepath)
        
        # 遍历所有工作表
        for sheet_name in xls.sheet_names:
            try:
                df = pd.read_excel(xls, sheet_name=sheet_name)
                
                # 获取标题行
                headers = df.columns.tolist()
                
                # 搜索关键字
                mask = df.apply(lambda row: row.astype(str).str.contains(keyword, case=False, na=False).any(), axis=1)
                matched_rows = df[mask]
                
                if not matched_rows.empty:
                    # 将匹配的行转换为字典列表
                    matched_data = matched_rows.to_dict('records')
                    
                    # 添加工作表信息
                    results.append({
                        'sheet_name': sheet_name,
                        'headers': headers,
                        'data': matched_data
                    })
            except Exception as e:
                print(f"Error processing sheet {sheet_name}: {e}")
                continue
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        flash('读取Excel文件时出错，请检查文件格式')
    
    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 检查是否有文件上传
        file = None
        filename = None
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                if file and allowed_file(file.filename):
                    # 处理中文文件名
                    filename = secure_filename_custom(file.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    session['selected_file'] = filename  # 保存选择的文件到session
                    flash('文件上传成功')
                else:
                    flash('只允许上传Excel文件 (.xlsx, .xls)')
                    return redirect(request.url)
        
        # 获取关键字和选择的文件
        keyword = request.form.get('keyword', '').strip()
        selected_file = request.form.get('selected_file', '')
        
        if not keyword:
            flash('请输入搜索关键字')
            return redirect(request.url)
        
        # 确定要搜索的文件
        if filename:  # 优先使用新上传的文件
            file_to_search = filename
        elif selected_file:  # 然后使用表单中选择的文件
            file_to_search = selected_file
            session['selected_file'] = selected_file
        elif 'selected_file' in session:  # 最后使用session中保存的文件
            file_to_search = session['selected_file']
        else:
            flash('请选择或上传一个Excel文件')
            return redirect(request.url)
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file_to_search)
        
        # 搜索关键字
        results = search_in_excel(filepath, keyword)
        
        if not results:
            flash(f'未找到包含 "{keyword}" 的内容')
            return redirect(request.url)
        
        return render_template('results.html', 
                             keyword=keyword, 
                             filename=file_to_search, 
                             results=results)
    
    # GET请求 - 显示表单
    uploaded_files = get_uploaded_files()
    return render_template('index.html', 
                         uploaded_files=uploaded_files,
                         selected_file=session.get('selected_file', ''))

# 确保模板渲染时使用正确的编码
@app.after_request
def add_header(response):
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response

if __name__ == '__main__':
    app.run(debug=True, port=8091)