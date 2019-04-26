#!/usr/bin/env python3

import sys

ov = 0
vo = 0

v_ind = set()
obj_head = []
with open(sys.argv[1], 'r', encoding='utf-8') as f:
    for l in f:
        if l.startswith('#'):
            continue
        if l.strip() == '': # end of a sentence
            ov += sum(i < head for i, head in obj_head if head in v_ind)
            vo += sum(head < i for i, head in obj_head if head in v_ind)
            v_ind.clear()
            obj_head.clear()
            continue
        i, _, _, pos, _, _, head, label, _, _ = l.split()
        if pos == 'VERB':
            v_ind.add(int(i))
        elif label == 'obj':
            obj_head.append( (int(i), int(head)) )

print(f'OV: {ov/(ov+vo):.2f}')
print(f'VO: {vo/(ov+vo):.2f}')
