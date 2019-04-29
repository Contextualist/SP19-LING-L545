#!/usr/bin/env python3

from nltk.tokenize import sent_tokenize
out = open('punkt.out', 'w', encoding='utf-8')
text = ''
with open('wiki.txt', 'r', encoding='utf-8') as f:
    for l in f:
        if l == '\n':
            out.write('\n'.join(sent_tokenize(text))+'\n')
            text = ''
            continue
        text += l
out.close()

