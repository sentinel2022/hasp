# 存储3条个人信息，并支持按姓名查询年龄和职业
# 运行方式：python personal_info.py

# 使用字典存储姓名对应的信息，代码简洁易读
people = {
    '张三': {'age': 28, 'job': '工程师'},
    '李四': {'age': 32, 'job': '教师'},
    '王五': {'age': 24, 'job': '设计师'},
}

# 从用户输入中读取姓名，并进行查询
name = input('请输入姓名：').strip()
info = people.get(name)
if info:
    print(f"{name} 的年龄是：{info['age']}，职业是：{info['job']}")
else:
    print('无此信息')