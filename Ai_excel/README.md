# Excel 搜索与编辑 Web 应用

快速启动：

1. 创建并进入虚拟环境，安装依赖：

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

2. 启动应用（支持网络访问）：

```powershell
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

3. 用浏览器打开：

http://<服务器IP>:8000/

说明：
- 上传 Excel 文件（.xlsx），选择文件，输入关键字后点击“搜索”。
- 搜索结果按工作表分组，显示表头并列出匹配的行，单元格可直接编辑并点击“保存”。
- 支持“新增记录”和“删除记录”。
- 为了速度，搜索使用 pandas 读取并做模糊匹配。大文件建议在更高性能机器上运行。
