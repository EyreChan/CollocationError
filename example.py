import json
from sup_LD import LD
text = open("test.txt", 'r', encoding = 'gbk')

dic = {}

for line in text:
    strs = line.rstrip().split(" ")
    for str in strs:
        LD(str, strs, dic)

