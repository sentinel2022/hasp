import sys
import pandas as pd
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QTableWidget, QTableWidgetItem, QFileDialog, 
                             QMessageBox, QHeaderView, QProgressBar, QComboBox)
from PyQt5.QtCore import Qt

class ExcelSearchApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Excel关键字查找工具 - 多工作表支持")
        self.setGeometry(100, 100, 1200, 800)
        
        # 初始化变量
        self.df_dict = {}  # 存储所有工作表的字典
        self.current_sheet = None
        self.header_labels = []
        
        # 创建中央部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 文件选择区域
        file_layout = QHBoxLayout()
        self.file_label = QLabel("未选择文件")
        self.browse_button = QPushButton("浏览Excel文件")
        self.browse_button.clicked.connect(self.browse_file)
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.browse_button)
        
        # 工作表选择区域
        sheet_layout = QHBoxLayout()
        self.sheet_combo = QComboBox()
        self.sheet_combo.currentTextChanged.connect(self.sheet_changed)
        sheet_layout.addWidget(QLabel("选择工作表:"))
        sheet_layout.addWidget(self.sheet_combo)
        
        # 搜索区域
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("输入要查找的关键字...")
        self.search_button = QPushButton("搜索")
        self.search_button.clicked.connect(self.search_keyword)
        search_layout.addWidget(QLabel("关键字:"))
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        
        # 结果表格
        self.result_table = QTableWidget()
        self.result_table.setAlternatingRowColors(True)
        
        # 添加到主布局
        layout.addLayout(file_layout)
        layout.addLayout(sheet_layout)
        layout.addLayout(search_layout)
        layout.addWidget(self.progress_bar)
        layout.addWidget(QLabel("搜索结果:"))
        layout.addWidget(self.result_table)
        
        # 状态栏
        self.statusBar().showMessage("就绪")
        
    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择Excel文件", "", "Excel文件 (*.xlsx *.xls)"
        )
        if file_path:
            self.file_label.setText(file_path)
            try:
                # 读取Excel文件的所有工作表
                excel_file = pd.ExcelFile(file_path)
                self.df_dict = {}
                
                # 清空工作表选择框
                self.sheet_combo.clear()
                
                # 遍历所有工作表
                for sheet_name in excel_file.sheet_names:
                    df = pd.read_excel(excel_file, sheet_name=sheet_name)
                    self.df_dict[sheet_name] = df
                    self.sheet_combo.addItem(sheet_name)
                
                # 默认选择第一个工作表
                if self.sheet_combo.count() > 0:
                    self.sheet_combo.setCurrentIndex(0)
                
                self.statusBar().showMessage(f"成功加载文件: {file_path}, 共 {len(self.df_dict)} 个工作表")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"无法读取文件: {str(e)}")
                self.file_label.setText("未选择文件")
    
    def sheet_changed(self, sheet_name):
        if sheet_name and sheet_name in self.df_dict:
            self.current_sheet = sheet_name
            self.header_labels = self.df_dict[sheet_name].columns.tolist()
            self.statusBar().showMessage(f"已切换到工作表: {sheet_name}")
    
    def search_keyword(self):
        if not self.df_dict:
            QMessageBox.warning(self, "警告", "请先选择Excel文件")
            return
            
        keyword = self.search_input.text().strip()
        if not keyword:
            QMessageBox.warning(self, "警告", "请输入要查找的关键字")
            return
            
        self.progress_bar.setVisible(True)
        
        try:
            # 收集所有工作表的搜索结果
            all_results = []
            total_sheets = len(self.df_dict)
            current_sheet_index = 0
            
            for sheet_name, df in self.df_dict.items():
                current_sheet_index += 1
                self.progress_bar.setValue(int((current_sheet_index / total_sheets) * 100))
                self.statusBar().showMessage(f"正在搜索工作表: {sheet_name} ({current_sheet_index}/{total_sheets})")
                QApplication.processEvents()  # 保持UI响应
                
                # 查找包含关键字的行
                for index, row in df.iterrows():
                    if any(str(cell).lower().find(keyword.lower()) != -1 for cell in row):
                        # 添加工作表名称到结果中
                        row_data = row.tolist()
                        row_data.insert(0, sheet_name)  # 在第一列添加工作表名称
                        all_results.append(row_data)
            
            # 显示结果
            self.display_results(all_results, keyword)
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"搜索过程中发生错误: {str(e)}")
        finally:
            self.progress_bar.setVisible(False)
    
    def display_results(self, results, keyword):
        if not results:
            self.result_table.setRowCount(0)
            self.result_table.setColumnCount(0)
            self.statusBar().showMessage(f"未找到包含 '{keyword}' 的结果")
            return
            
        # 设置表格行和列
        # 列数 = 原始列数 + 1 (添加的工作表名称列)
        column_count = len(results[0])
        self.result_table.setRowCount(len(results))
        self.result_table.setColumnCount(column_count)
        
        # 设置表头 (工作表名称 + 原始表头)
        headers = ["工作表名称"] + self.header_labels
        self.result_table.setHorizontalHeaderLabels(headers)
        
        # 填充数据
        for row_idx, row_data in enumerate(results):
            for col_idx, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                
                # 高亮显示匹配的关键字 (从第二列开始检查，因为第一列是工作表名称)
                if col_idx > 0 and str(cell_data).lower().find(keyword.lower()) != -1:
                    item.setBackground(Qt.yellow)
                
                self.result_table.setItem(row_idx, col_idx, item)
        
        # 调整列宽
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # 更新状态栏
        self.statusBar().showMessage(f"找到 {len(results)} 条包含 '{keyword}' 的结果")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExcelSearchApp()
    window.show()
    sys.exit(app.exec_())