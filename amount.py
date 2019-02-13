corpus = open('corpus.txt', 'r',encoding = 'utf-8-sig')

amount_corpus = 0;
for line in corpus:
    strs = line.rstrip('\n').split()
    for str in strs:
        amount_corpus = amount_corpus + 1
print(amount_corpus)