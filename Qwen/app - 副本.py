# app.py (完整修复版)
from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import os
import json
from datetime import datetime
import threading
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

class ExcelManager:
    def __init__(self):
        self.data_cache = {}
        self.lock = threading.Lock()
    
    def load_excel(self, filepath):
        with self.lock:
            if filepath not in self.data_cache:
                try:
                    excel_data = pd.read_excel(filepath, sheet_name=None, dtype=str)
                    for sheet_name in excel_data:
                        excel_data[sheet_name] = excel_data[sheet_name].fillna('')
                    self.data_cache[filepath] = excel_data
                except Exception as e:
                    raise Exception(f"加载Excel文件失败: {str(e)}")
            return self.data_cache[filepath]
    
    def save_excel(self, filepath, data):
        with self.lock:
            try:
                with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                    for sheet_name, df in data.items():
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
                self.data_cache[filepath] = data
            except Exception as e:
                raise Exception(f"保存Excel文件失败: {str(e)}")
    
    def search_keyword(self, filepath, keyword):
        data = self.load_excel(filepath)
        results = []
        keyword_lower = str(keyword).lower()
        
        for sheet_name, df in data.items():
            if df.empty:
                continue
            columns = df.columns.tolist()
            mask = df.astype(str).apply(lambda x: x.str.lower().str.contains(keyword_lower, na=False)).any(axis=1)
            matching_rows = df[mask]
            
            if not matching_rows.empty:
                for idx, row in matching_rows.iterrows():
                    results.append({
                        'sheet_name': sheet_name,
                        'row_index': int(idx),
                        'columns': columns,
                        'data': row.tolist(),
                        'original_index': int(idx)
                    })
        return results
    
    def update_cell(self, filepath, sheet_name, row_index, column_index, new_value):
        data = self.load_excel(filepath)
        if sheet_name in data and row_index < len(data[sheet_name]):
            columns = data[sheet_name].columns.tolist()
            if column_index < len(columns):
                data[sheet_name].iloc[row_index, column_index] = new_value
                self.save_excel(filepath, data)
                return True
        return False
    
    def add_row(self, filepath, sheet_name, row_data):
        data = self.load_excel(filepath)
        if sheet_name in data:
            new_row = pd.DataFrame([row_data], columns=data[sheet_name].columns)
            data[sheet_name] = pd.concat([data[sheet_name], new_row], ignore_index=True)
            self.save_excel(filepath, data)
            return True
        return False
    
    def delete_row(self, filepath, sheet_name, row_index):
        data = self.load_excel(filepath)
        if sheet_name in data and row_index < len(data[sheet_name]):
            data[sheet_name] = data[sheet_name].drop(data[sheet_name].index[row_index]).reset_index(drop=True)
            self.save_excel(filepath, data)
            return True
        return False
    
    def get_sheet_names(self, filepath):
        data = self.load_excel(filepath)
        return list(data.keys())
    
    def get_sheet_columns(self, filepath, sheet_name):
        data = self.load_excel(filepath)
        if sheet_name in data:
            return data[sheet_name].columns.tolist()
        return []

excel_manager = ExcelManager()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'xlsx', 'xls'}

@app.route('/')
def index():
    files_list = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if filename.endswith(('.xlsx', '.xls')):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            stat = os.stat(filepath)
            files_list.append({
                'filename': filename,
                'size': stat.st_size,
                'upload_time': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            })
    return render_template('index.html', uploaded_files=files_list)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': '没有选择文件'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': '没有选择文件'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        if os.path.exists(filepath):
            name, ext = os.path.splitext(filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{name}_{timestamp}{ext}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        file.save(filepath)
        
        try:
            pd.read_excel(filepath, sheet_name=None)
            return jsonify({
                'success': True, 
                'message': '文件上传成功',
                'filename': filename
            })
        except Exception as e:
            os.remove(filepath)
            return jsonify({'success': False, 'message': f'无效的Excel文件: {str(e)}'})
    
    return jsonify({'success': False, 'message': '不支持的文件格式'})

@app.route('/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        filename = data.get('filename')
        keyword = data.get('keyword', '')
        
        if not filename or not keyword:
            return jsonify({'success': False, 'message': '缺少必要参数'})
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(filepath):
            return jsonify({'success': False, 'message': '文件不存在'})
        
        results = excel_manager.search_keyword(filepath, keyword)
        
        return jsonify({
            'success': True,
            'results': results,
            'total': len(results)
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'搜索失败: {str(e)}'})

@app.route('/update_cell', methods=['POST'])
def update_cell():
    try:
        data = request.get_json()
        filename = data.get('filename')
        sheet_name = data.get('sheet_name')
        row_index = data.get('row_index')
        column_index = data.get('column_index')
        new_value = data.get('new_value')
        
        if None in [filename, sheet_name, row_index, column_index]:
            return jsonify({'success': False, 'message': '缺少必要参数'})
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(filepath):
            return jsonify({'success': False, 'message': '文件不存在'})
        
        success = excel_manager.update_cell(filepath, sheet_name, row_index, column_index, new_value)
        
        if success:
            return jsonify({'success': True, 'message': '更新成功'})
        else:
            return jsonify({'success': False, 'message': '更新失败'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'更新失败: {str(e)}'})

@app.route('/add_row', methods=['POST'])
def add_row():
    try:
        data = request.get_json()
        filename = data.get('filename')
        sheet_name = data.get('sheet_name')
        row_data = data.get('row_data')
        
        if not filename or not sheet_name or not row_data:
            return jsonify({'success': False, 'message': '缺少必要参数'})
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(filepath):
            return jsonify({'success': False, 'message': '文件不存在'})
        
        success = excel_manager.add_row(filepath, sheet_name, row_data)
        
        if success:
            return jsonify({'success': True, 'message': '添加成功'})
        else:
            return jsonify({'success': False, 'message': '添加失败'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'添加失败: {str(e)}'})

@app.route('/delete_row', methods=['POST'])
def delete_row():
    try:
        data = request.get_json()
        filename = data.get('filename')
        sheet_name = data.get('sheet_name')
        row_index = data.get('row_index')
        
        if None in [filename, sheet_name, row_index]:
            return jsonify({'success': False, 'message': '缺少必要参数'})
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(filepath):
            return jsonify({'success': False, 'message': '文件不存在'})
        
        success = excel_manager.delete_row(filepath, sheet_name, row_index)
        
        if success:
            return jsonify({'success': True, 'message': '删除成功'})
        else:
            return jsonify({'success': False, 'message': '删除失败'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'删除失败: {str(e)}'})

@app.route('/get_sheet_info', methods=['POST'])
def get_sheet_info():
    try:
        data = request.get_json()
        filename = data.get('filename')
        
        if not filename:
            return jsonify({'success': False, 'message': '缺少必要参数'})
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(filepath):
            return jsonify({'success': False, 'message': '文件不存在'})
        
        sheet_names = excel_manager.get_sheet_names(filepath)
        sheet_info = {}
        for sheet_name in sheet_names:
            columns = excel_manager.get_sheet_columns(filepath, sheet_name)
            sheet_info[sheet_name] = columns
        
        return jsonify({
            'success': True,
            'sheet_info': sheet_info
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'获取工作表信息失败: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)