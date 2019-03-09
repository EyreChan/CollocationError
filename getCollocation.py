from amount import amount_corpus
from LDistance import dic, w_dic, d_dic, LD_interv
import math
from copy import deepcopy
import json
import re

corpus = open('corpus.txt', 'r', encoding = 'utf-8-sig')

mi_dic = deepcopy(dic)      #避免计算互信息时对dic造成影响
d_temp_dic = deepcopy(dic)  #
d_num_dic = {}

datalist1 = []              #搭配词左
datalist2 = []              #搭配词右
dict_match = {}             #搭配词典
dict_match_converse = {}    #搭配词典k-v倒置

#计算互信息MI/搭配强度
def mi(str1, str2):
    if (str1 + ' ' + str2) in mi_dic:
        mi_num = math.log((amount_corpus*dic[str1 + ' ' + str2])/(w_dic[str1]*w_dic[str2]), 2)
        mi_dic.pop(str1 + ' ' + str2)
        return mi_num;
    else:
        return 1;

#语料库中窗口大小内共现的次数
def frq(str1, str2):
    sum = dic[str1 + ' ' + str2]
    return sum

def ave_frq(str1, str2):
    sum = frq(str1, str2)
    ave_f = sum / LD_interv
    return ave_f

#计算搭配离散度DISP
def disp(str1, str2):
    ave_f = ave_frq(str1, str2)
    temp_sum = 0
    for i in range(1, LD_interv + 1, 1):
        str = str1 + ' ' + str2
        str_i = str1 + ' ' + str2 + '%d'%i
        if str in d_temp_dic and str_i in d_dic:
            temp_sum = temp_sum + pow(d_dic[str_i] - ave_f, 2)
            d_temp_dic.pop(str)
    d_num = temp_sum / LD_interv
    d_num_dic[str] = d_num
    return d_num

#计算尖峰值
def peak(str1, str2, i):
    p_num = 1
    frq = d_dic[str1 + ' ' + str2 + '%d'%i]
    ave_f = ave_frq(str1, str2)
    d_n = d_num_dic[str1 + ' ' + str2]
    if d_n > 0:
        p_num = (frq - ave_f)/math.sqrt(d_n)
    return p_num

def isPeak(str1, str2):
    ave_f = ave_frq(str1, str2)
    max_peak = 0
    num = 0
    for i in range(1, LD_interv + 1):
        str_i = str1 + ' ' + str2 + '%d'%i
        if str_i in d_dic:
            if d_dic[str_i] > max_peak:
                max_peak = d_dic[str_i]
                num = i
    if 0.3 <= ave_f and ave_f < 1.0 and peak(str1, str2, num) >= 2.5:
        is_peak = 1
    elif 1.0 <= ave_f and ave_f < 5.0 and peak(str1, str2, num) >= 2.0:
        is_peak = 1
    elif 5.0 <= ave_f and ave_f < 10.0 and peak(str1, str2, num) >= 1.5:
        is_peak = 1
    elif ave_f >= 10.0 and peak(str1, str2, num) > 1.0:
        is_peak = 1
    else:
        is_peak = 0;
    return is_peak

def add_dic(str1, str2):
    datalist1.append(str1)
    datalist2.append(str2)
    return

for line in corpus:
    strs = line.rstrip('\n').split();
    for str in strs:
        max_num = min(len(strs) - strs.index(str) - 1, LD_interv)
        for i in range(1, max_num + 1, 1):
            str_i = strs[strs.index(str) + i]
            #要求共现至少5次
            #if frq(str, str_i) > 5:
            mi_num = mi(str, str_i)
            d_num = disp(str, str_i)
            #参数未定
            if  mi_num >= 5:
                add_dic(str, str_i)
            elif mi_num < 3 and mi_num >= 5 and d_num > 10:
                add_dic(str, str_i)
            elif mi_num < 2.5 and mi_num >= 3 and d_num > 20:
                add_dic(str, str_i)
            elif mi_num <= 2.5:
                if isPeak(str, str_i):
                    add_dic(str, str_i)

for i in range(0, len(datalist1)):
    if datalist1[i] not in dict_match:
        dict_match[datalist1[i]] = []
        dict_match[datalist1[i]].append(datalist2[i])
    elif datalist1[i] in dict_match:
        if datalist2[i] in dict_match[datalist1[i]]:
            pass
        else:
            dict_match[datalist1[i]].append(datalist2[i])

if "正文" in dict_match:
    dict_match.pop("正文")
if "已有" in dict_match:
    dict_match.pop("已有")
if "条岁" in dict_match:
    dict_match.pop("条岁")
if "商震" in dict_match:
    dict_match.pop("商震")
if "兼" in dict_match:
    dict_match.pop("兼")
if "三轮车夫" in dict_match:
    dict_match.pop("三轮车夫")
if "光明网" in dict_match:
    dict_match.pop("光明网")
if "陈长" in dict_match:
    dict_match.pop("陈长")

for key in dict_match:
    if "正文" in dict_match[key]:
        dict_match[key].remove("正文")
    if "已有" in dict_match[key]:
        dict_match[key].remove("已有")
    if "条岁" in dict_match[key]:
        dict_match[key].remove("条岁")
    if "商震" in dict_match[key]:
        dict_match[key].remove("商震")
    if "兼" in dict_match[key]:
        dict_match[key].remove("兼")
    if "三轮车夫" in dict_match[key]:
        dict_match[key].remove("三轮车夫")
    if "光明网" in dict_match[key]:
        dict_match[key].remove("光明网")
    if "陈长" in dict_match[key]:
        dict_match[key].remove("陈长")

#k-v反转
for k, vlist in dict_match.items():
    for v in vlist:
        dict_match_converse.setdefault(v, []).append(k)

with open("LD_collocation.json", "w", encoding='utf-8') as f1:
    f1.writelines(json.dumps(dict_match, ensure_ascii=False, indent=4))
with open("LD_collocation_converse.json", "w", encoding='utf-8') as f2:
    f2.writelines(json.dumps(dict_match_converse, ensure_ascii=False, indent=4))