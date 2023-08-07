message = """
这是一个\t带有\t\t制表符的
多行字符串。
"""
print(message)

fruits = ['apple', 'banana', 'orange']
for index, fruit in enumerate(fruits, start=2):
    print(index, fruit)