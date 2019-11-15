import re
str1 = "Duplicate entry '清华大学出版社' for key 'name'"
# reg = r"Duplicate entry \'(*.)\' for key \'name\'"
reg = r"Duplicate entry '(.*?)' for key 'name'"
ss = re.findall(reg,str1)
if ss:
    print(ss[0])
else:
    print("没有匹配到")