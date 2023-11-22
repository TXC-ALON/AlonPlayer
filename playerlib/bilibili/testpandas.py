import pandas as pd

# 创建一个DataFrame
data = {'Name': ['Alice', 'Bob', 'Charlie', 'David'],
        'Age': [25, 32, 18, 47],
        'City': ['Beijing', 'Shanghai', 'Guangzhou', 'Shenzhen']}
df = pd.DataFrame(data)

# 将DataFrame保存为Excel文件
df.to_excel('output.xlsx', index=False)