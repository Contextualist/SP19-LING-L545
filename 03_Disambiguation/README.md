## Tagger Comparison

### UDPipe

```
> git clone https://github.com/ufal/udpipe
> cd udpipe/src
> make
> cat UD_Finnish-TDT/fi_tdt-ud-train.conllu | udpipe/src/udpipe --tokenizer=none --parser=none --train fi.udpipe
> cat UD_Finnish-TDT/fi_tdt-ud-test.conllu | udpipe/src/udpipe --tag fi.udpipe > fi_tdt-ud-test_output.conllu
> python3 conll17_ud_eval.py --verbose UD_Finnish-TDT/fi_tdt-ud-test.conllu fi_tdt-ud-test_output.conllu

Metrics    | Precision |    Recall |  F1 Score | AligndAcc
-----------+-----------+-----------+-----------+-----------
...
UPOS       |     94.64 |     94.64 |     94.64 |     94.64
...
```

Most common errors:
```
udpipe
128	PROPN	NOUN
100	VERB	NOUN
99	ADJ	NOUN 
```

### perceptron

```
> git clone https://github.com/ftyers/conllu-perceptron-tagger
> cat UD_Finnish-TDT/fi_tdt-ud-train.conllu | python conllu-perceptron-tagger/tagger.py -t perceptron.model.dat
> cat UD_Finnish-TDT/fi_tdt-ud-test.conllu | python conllu-perceptron-tagger/tagger.py perceptron.model.dat > perceptron_output.conllu
> python evaluation_script/conll17_ud_eval.py --verbose UD_Finnish-TDT/fi_tdt-ud-test.conllu perceptron_output.conllu 

Metrics    | Precision |    Recall |  F1 Score | AligndAcc
-----------+-----------+-----------+-----------+-----------
...
UPOS       |     90.39 |     90.39 |     90.39 |     90.39
...
```

Most common errors:
```
perceptron
319	VERB	NOUN
315	ADJ	NOUN
164	NOUN	VERB
```

### Hunpos

```
> curl -L https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/hunpos/hunpos-1.0-linux.tgz | tar xz
> conllu2pos() { grep -v "^#" | awk -v OFS='\t' '{print $2, $4}'| awk -v OFS='\t' '{$1=$1};1'; }
> cat UD_Finnish-TDT/fi_tdt-ud-train.conllu | conllu2pos > fi_train.hunpos.txt
> cat fi_train.hunpos.txt | hunpos-1.0-linux/hunpos-train hunpos.model.dat
>
> cat UD_Finnish-TDT/fi_tdt-ud-test.conllu | conllu2pos > fi_test.hunpos.txt
> cat fi_test.hunpos.txt | awk '{print $1}' > fi_test.hunpos.input
> hunpos-1.0-linux/hunpos-tag hunpos.model.dat < fi_test.hunpos.input | awk -v OFS='\t' '{$1=$1};1' > fi_test.hunpos.output
> 
> TOTAL=`cat fi_test.hunpos.txt | grep -v '^$' | wc -l`
> ERROR=`diff -U 0 fi_test.hunpos.output fi_test.hunpos.txt | grep ^@ | wc -l`
> python -c "print((${TOTAL}-${ERROR})/${TOTAL}*100)"

94.01993355481729
```

Most common errors:
```
hunpos
167	VERB	NOUN
146	PROPN	NOUN
135	ADJ	NOUN
```

## Constraint Grammar

See [rus.cg3](rus.cg3), [input.txt](input.txt), and [output.txt](output.txt).

## Improve perceptron tagger

The target language is Finnish. Because Finnish is quite synthetic, and the inflections are mostly suffixes, so I increase the length of suffixes in feature extraction:

```diff
@@ -162,20 +162,20 @@ class PerceptronTagger():
                i += len(self.START)
                features = defaultdict(int)
                # It's useful to have a constant feature, which acts sort of like a prior
                add('bias')
-               add('i suffix', word[-3:])
+               add('i suffix', word[-5:])
                add('i pref1', word[0])
                add('i-1 tag', prev)
                add('i-2 tag', prev2)
                add('i tag+i-2 tag', prev, prev2)
                add('i word', context[i])
                add('i-1 tag+i word', prev, context[i])
                add('i-1 word', context[i-1])
-               add('i-1 suffix', context[i-1][-3:])
+               add('i-1 suffix', context[i-1][-5:])
                add('i-2 word', context[i-2])
                add('i+1 word', context[i+1])
-               add('i+1 suffix', context[i+1][-3:])
+               add('i+1 suffix', context[i+1][-5:])
                add('i+2 word', context[i+2])
                #print(word, '|||', features)
                return features
```

Using `UPOS` as the metric for the tagger's performance, the baseline is 90.39%

```
 suffix length | UPOS
---------------+--------
 3 (default)   | 90.39%
 4             | 91.53%
 5             | 92.03%
 6             | 91.51%
```

When the length of sampling suffixes is 5, the perceptron can concentrate on the most important features.
