import pandas as pd

try:
    from pypinyin import lazy_pinyin, Style
except ImportError:
    lazy_pinyin = None

# 步骤2: 读取Excel文件的所有工作表
excel_file = pd.ExcelFile('example.xlsx')
sheet_names = excel_file.sheet_names
dfs = {sheet: excel_file.parse(sheet) for sheet in sheet_names}

# 目标列名称
possible_columns = ['Name', '姓名']

# 步骤3: 将汉字转换为拼音首字母

def convert_to_pinyin_initials(value):
    if not isinstance(value, str) or len(value) == 0:
        return value
    if lazy_pinyin is None:
        raise ImportError(
            '未安装 pypinyin，无法将汉字转换为拼音首字母。请运行: pip install pypinyin'
        )
    initials = lazy_pinyin(value, style=Style.FIRST_LETTER, errors='default')
    return ''.join(item[0].upper() for item in initials if item)

# 处理每个工作表
for sheet_name, df in dfs.items():
    target_column = next((col for col in possible_columns if col in df.columns), None)
    if target_column is None:
        print(f"警告: 工作表 '{sheet_name}' 中没有任何列 {possible_columns}，跳过。")
        continue

    new_column = f"{target_column}_pinyin"
    if new_column in df.columns:
        print(f"警告: 工作表 '{sheet_name}' 中 '{new_column}' 列已存在，跳过。")
        continue

    insert_position = df.columns.get_loc(target_column)
    pinyin_values = df[target_column].apply(convert_to_pinyin_initials)
    df.insert(insert_position, new_column, pinyin_values)
    print(f"工作表 '{sheet_name}' 的 '{target_column}' 列已转换为拼音首字母。")

# 步骤4: 写回Excel文件
with pd.ExcelWriter('modified_example.xlsx') as writer:
    for sheet_name, df in dfs.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)

