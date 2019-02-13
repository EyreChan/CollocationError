corpus = open('corpus.txt', 'r',encoding = 'utf-8-sig')

dic = {}    #记录搭配出现的次数
w_dic = {}  #记录词语出现的次数
d_dic = {}  #记录某距离搭配出现的次数

LD_interv = 5
for line in corpus:
    strs = line.rstrip('\n').split()
    for str in strs:
        max_num = min(len(strs) - strs.index(str) - 1, LD_interv)
        for i in range(1, max_num + 1, 1):
            if (str + ' ' + strs[strs.index(str) + i]) not in dic:
                dic[str + ' ' + strs[strs.index(str) + i]] = 1
            elif (str + ' ' + strs[strs.index(str) + i]) in dic:
                dic[str + ' ' + strs[strs.index(str) + i]] = dic[str + ' ' + strs[strs.index(str) + i]] + 1
            str_i = str + ' ' + strs[strs.index(str) + i] + '%d'%i
            if str_i in d_dic:
                d_dic[str_i] = d_dic[str_i] + 1
            else:
                d_dic[str_i] = 1
        if str in w_dic:
            w_dic[str] = w_dic[str] + 1
        else:
            w_dic[str] = 1
