#!/usr/bin/env python3

import sys

sep = ' '

def tokenize(s):
    while len(s) > 0:
        for i in reversed(range(1, len(s)+1)):
            if s[:i] in d:
                print(s[:i], end=sep)
                s = s[i:]
                break
        else:
            print(s[:1], end=sep)
            s = s[1:]
    print()


d = set()
with open(sys.argv[1], 'r', encoding='utf-8') as f:
    for l in f:
        d.add(l[:-1])

with open(0) as f:
    for l in f:
        tokenize(l[:-1])
