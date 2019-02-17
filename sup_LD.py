import json
from pypinyin import lazy_pinyin
from copy import deepcopy

with open("homophone.json","r",encoding='utf-8') as f:
    py_dic = json.load(f)
with open("LD_collocation.json","r",encoding='utf-8') as f1:
    match_dic = json.load(f1)
with open("LD_collocation_converse.json","r",encoding='utf-8') as f2:
    match_c_dic = json.load(f2)

list = []

LD_interv = 5

def isCollocation(str, sup_list, error_list):
    if str not in sup_list:
        if len(sup_list) >= 1:
            if str in error_list:
                for i in range(0, len(sup_list)):
                    if sup_list[i] not in error_list[str]:
                        error_list[str].append(sup_list[i])
            else:
                error_list[str] = []
                for i in range(0, len(sup_list)):
                    error_list[str].append(sup_list[i])
    return

def LD(str, strs, error_list):
    sup_dic = {}
    sup_dic[str] = 0
    r_max = min(len(strs) - strs.index(str) - 1, LD_interv)
    l_max = min(strs.index(str), LD_interv)
    if str in match_dic:
        for i in range(1, r_max + 1, 1):
            if strs[strs.index(str) + i] in match_dic[str]:
                sup_dic[str] = sup_dic[str] + 1
    if str in match_c_dic:
        for i in range(1, l_max + 1, 1):
            if strs[strs.index(str) - i] in match_c_dic[str]:
                sup_dic[str] = sup_dic[str] + 1
    py_str = " ".join(lazy_pinyin(str))
    max_sup = sup_dic[str]
    if py_str in py_dic and (len(py_dic[py_str]) > 1):
        sup_list = []
        sup_list.append(str)
        temp_dic = deepcopy(py_dic)
        if str in temp_dic[py_str]:
            temp_dic[py_str].remove(str)
        for s in temp_dic[py_str]:
            sup_dic[s] = 0
            if s in match_dic:
                for i in range(1, r_max + 1, 1):
                    if strs[strs.index(str) + i] in match_dic[s]:
                        sup_dic[s] = sup_dic[s] + 1
            if s in match_c_dic:
                for i in range(1, l_max + 1, 1):
                    if strs[strs.index(str) - i] in match_c_dic[s]:
                        sup_dic[s] = sup_dic[s] + 1
            if sup_dic[s] > max_sup:
                max_sup = sup_dic[s]
                sup_list = []
                sup_list.append(s)
        isCollocation(str, sup_list, error_list)
    return



