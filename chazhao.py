import pandas as pd

def search_excel(file_path):
    # 读取Excel文件
    df = pd.read_excel(file_path)
    
    # 获取用户输入的关键词
    keyword = input("请输入关键词：")
    
    # 查找包含关键词的行
    result = df[df.apply(lambda row: keyword in ' '.join(map(str, row)), axis=1)]
    
    # 输出标题栏
    title = list(df.columns)
    print(f"标题栏: {title}")
    print()
    
    # 输出查找到的整行内容
    for row in result.iterrows():
        print(row[1].tolist())

# 调用search_excel函数
search_excel("3.xlsx")
