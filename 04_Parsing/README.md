## Train, parse and evaluate using UDPipe

Treebank [UD\_Classical\_Chinese-Kyoto](https://github.com/UniversalDependencies/UD_Classical_Chinese-Kyoto) is used for the analysis. The gold standard test file is [`lzh_kyoto-ud-test.conllu`](lzh_kyoto-ud-test.conllu), and the UDPipe output is [`cchn-test.out.conllu`](cchn-test.out.conllu).

### Evaluation

```
Metrics    | Precision |    Recall |  F1 Score | AligndAcc
-----------+-----------+-----------+-----------+-----------
Tokens     |    100.00 |    100.00 |    100.00 |
Sentences  |    100.00 |    100.00 |    100.00 |
Words      |    100.00 |    100.00 |    100.00 |      
UPOS       |    100.00 |    100.00 |    100.00 |    100.00
XPOS       |    100.00 |    100.00 |    100.00 |    100.00
Feats      |    100.00 |    100.00 |    100.00 |    100.00
AllTags    |    100.00 |    100.00 |    100.00 |    100.00
Lemmas     |    100.00 |    100.00 |    100.00 |    100.00
UAS        |     84.39 |     84.39 |     84.39 |     84.39
LAS        |     79.61 |     79.61 |     79.61 |     79.61
```

### Error Samples

Note: short sentences that consists of no more than 5 charcters are very prone to wrong labels.

1. `sent_id = KR1h0004_001_par2_8-16`: The second character of a multi-character verb is labeled as the object of the verb.
2. `sent_id = KR1h0004_001_par2_17-29`: The object of a clausal complement is labeled as an object paralled with it. (Opposite situation of #1)
3. `sent_id = KR1h0004_001_par4_4-9`: The subject of the sentence is labeled as the determiner of an adverbial modifier(a noun) right next to it.
4. `sent_id = KR1h0004_001_par5_17-20`: A adverbial clause is labeled as clausal complement. (Decision on whether the clause is a core complement)
5. `sent_id = KR1h0004_001_par7_4-7`: A verb pharse(VERB+obj) is recognized as a noun pharse(amod+NOUN). (Ambiguity of PoS and function in Chinese)
6. `sent_id = KR1h0004_001_par7_15-20`: A parataxia is labeled as a conjunct.
7. `sent_id = KR1h0004_001_par12_4-9`: The subject of a clause is labeled as the object of a preceding clause. (These are the two ways to interpret the sentence, because classic Chinese does not have punctuation.)
8. `sent_id = KR1h0004_001_par15_50-58`: An adverb that modifies a verb is labeled as the adverb that modifies an auxillary that modifies the verb.
9. `sent_id = KR1h0004_002_par3_3-6`: The root clause is swapped with its averbial clause (both in structure of NOUN-VERB).
10. Many instances: Confuse coordinating conjunction(cc) -- VERB with adverbial modifier(advmod) -- VERB.

## Relative word order study

See [wordorder.py](wordorder.py) and [wordorder.png](wordorder.png).
