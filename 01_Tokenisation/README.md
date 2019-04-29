## Sentence Segmentation

The corpus I used is one of the article bundles of enwiki, [enwiki-20190120-pages-articles14.xml-p7697599p7744799.bz2](https://dumps.wikimedia.org/enwiki/20190120/enwiki-20190120-pages-articles14.xml-p7697599p7744799.bz2) (11.3 MB). To evaluate the result, I compared the two outputs ([prag.out](segmentation/prag.out) and [punkt.out](segmentation/punkt.out)) with `diff`.

Among more than 100,000 sentences (100,813 for Pragmatic Segmenter, and 102,942 for Punkt), there's 2,472 differences. I manually inspected the differences in the first 2,000 sentences. All of the differences turned out to be the faults of Punkt.

### [Pragmatic Segmenter](https://github.com/diasks2/pragmatic_segmenter)

One feature for the Pragmatic Segmenter is to treat all sentences within a quote, no matter how long, as one sentence.

Pragmatic Segmenter yields good result for quotes: `...something like "Brad Whitford, what do you got to show for yourself?" or "What do you got up your sleeve?"`

I did not notice any case of failure for Pragmatic Segmenter.

### NLTK’s [Punkt](https://kite.com/python/docs/nltk.tokenise.punkt)

Failed cases:

* "number" (`no. //3`)
* nested quote (`This shark was referred to as ""Glyphis" sp. //C" until 2008`)
* title (`...received the degrees of B.S. //and E.E. //at the City College of New York...`); no segmentation when title abbr is the last word (`...against Fenerbahçe S.K.. On 17 September 2016, he...`)
* vs., i.e., e.g. (`e.g. //the state of Maryland, the state of California, US.`)
* punctuation with no space (`...three Veetons are missing.The Dragon From ...`)
* sentences within a quote (`"Danger! //Quagmire!".`)

Assume that all differences are Punk's error, its accuracy percentage is about 97.59%

---

## Tokenization

See [tokenization/maxmatch.py](tokenization/maxmatch.py).

Extract dictionary:
```bash
cat UD_Japanese-GSD/ja_gsd-ud-train.conllu | grep -E "^\d" | awk '{print $2}' | sort -u > dict.txt
```

Evaluate `maxmatch.py`:
```bash
$ cat UD_Japanese-GSD/ja_gsd-ud-test.conllu | grep "^# text" | awk '{print $4}' > test.txt
$ cat test.txt | python maxmatch.py dict.txt > hyp.txt

$ cat UD_Japanese-GSD/ja_gsd-ud-test.conllu | grep -v '^#' | awk '{print $2}' | awk 'NF {TMP=TMP $0 " "; next} {print TMP; TMP=""} END {print TMP}' > ref.txt
$ python2 wer.py ref.txt hyp.txt
Average WER for 553 words: 28.20 %
```

Word Error Rate is 28.20%.

`wer.py` is adapted from [zszyellow/WER-in-python](https://github.com/zszyellow/WER-in-python) with following changes in order to stat multiple sentences.
```diff
@@ -193,12 +193,17 @@
 
     # print the result in aligned way
     result = float(d[len(r)][len(h)]) / len(r) * 100
-    result = str("%.2f" % result) + "%"
-    alignedPrint(list, r, h, result)
+    return result
 
 if __name__ == '__main__':
     filename1 = sys.argv[1]
     filename2 = sys.argv[2]
-    r = file(filename1).read().split()
-    h = file(filename2).read().split()
-    wer(r, h)   
+    f1 = file(filename1).read().split('\n')
+    f2 = file(filename2).read().split('\n')
+    n = len(f1)
+    ans = 0
+    for i in range(n):
+        if f1[i] == '':
+            continue
+        ans += wer(f1[i].split(), f2[i].split())
+    print "Average WER for", n, "words:", "%.2f"%(ans/n), "%"
```
