class Item:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

    def __lt__(self, other):
        if self.name == other.name:
            return self.grade < other.grade
        else:
            return self.name < other.name


# 自定义元素列表
items = [
    Item('Alice', 85),
    Item('Bob', 92),
    Item('Alice', 78),
    Item('Charlie', 90),
    Item('Bob', 80)
]

# 多重排序
sorted_items = sorted(items)

# 打印排序结果
for item in sorted_items:
    print(item.name, item.grade)
