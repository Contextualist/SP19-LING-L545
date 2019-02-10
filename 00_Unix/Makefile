.PHONY: clean count-word fold-case vowel-seq freq rhyme bigram grep-count sed-count

wiki.txt:
	env python3 WikiExtractor.py --infn jbowiki-20190101-pages-articles.xml.bz2

clean:
	rm wiki.*

wiki.token: wiki.txt
	gsed "s/[^a-zA-Z\'\.\,]\+/\n/g" < wiki.txt > wiki.token

# 1. Count words in a text
count-word: wiki.token
	cat wiki.token | \
	sort -r | \
	uniq -c > wiki.hist

# 2. More counting exercises
fold-case:
	gsed 's/\(.*\)/\L\1/' < wiki.txt | \
	gsed "s/[^a-zA-Z\'\.\,]\+/\n/g" | \
	sort -r | \
	uniq -c > wiki.hist

vowel-seq:
	gsed 's/\(.*\)/\L\1/' < wiki.txt | \
	gsed "s/[^aeiouy]\+/\n/g" | \
	sort -r | \
	uniq -c > wiki.vowel.hist

# 3. Sort
freq: wiki.token
	cat wiki.token | \
	sort | \
	uniq -c | \
	sort -nr > wiki.freq.hist

rhyme: wiki.token
	cat wiki.token | \
	rev | \
	sort | \
	rev | \
	uniq -c > wiki.rhyme.hist

# 4. Bigrams
bigram: wiki.token
	cat wiki.token | grep -v '^$$' > wiki.words
	tail -n +2 wiki.words > wiki.nextwords
	paste wiki.words wiki.nextwords | sort | uniq -c > wiki.bigrams
	rm wiki.words wiki.nextwords

# 6. grep: An Example of a Filter
grep-count: wiki.token
	# uppercase
	grep -c "^[A-Z\'\.\,]\+$$" wiki.token
	# lowercase
	grep -c "^[a-z\'\.\,]\+$$" wiki.token
	# 4-letter
	grep -c "^....$$" wiki.token
	# no vowel
	grep -c '^[^aeiouy]\+$$' wiki.token
	# 1-syllable
	grep -c '^[^aeiouy]*[aeiouy][^aeiouy]*$$' wiki.token
	# 2-syllable
	grep -c '^[^aeiouy]*[aeiouy][^aeiouy]*[aeiouy][^aeiouy]*$$' wiki.token

# 7. sed (stream editor)
sed-count: wiki.token
	# initial consonant seq
	gsed 's/^\([^aeiouy]*\).*/\1/g' < wiki.token | sort -fu | wc -l
	# final consonant seq
	cat wiki.token | rev | \
	gsed 's/^\([^aeiouy]*\).*/\1/g' | sort -fu | wc -l
