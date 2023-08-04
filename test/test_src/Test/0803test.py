import math
NaN = math.nan

print(NaN)
print(1+NaN)
print(1e6)

class person:
    def __init__(self, _name, _age):
        self.name = _name
        self.age = _age

def compare_person(p):
    return ( p.name,-p.age)  # 按姓名递增，年龄递减排序

Anna = person("anna", 13)
Bnna = person("anna", 15)
Bnna2 = person("bnna", 15)
Cnna = person("cnna", 16)
personlist = [Anna, Bnna, Bnna2,Cnna]

sorted_personlist = sorted(personlist, key=compare_person)

for p in sorted_personlist:
    print(p.name, p.age)