.PHONY: compose-chv coverage paradigm guesser restrict prob clean
# build-% build2-% compose-% graph-% string-% txt-% take a language token (e.g. chv, ava, fin)

hb = "hfst/bin/hfst-"# Modify this to the path/to/hfst/bin/hfst-

%.lexc.hfst: %.lexc
	${hb}lexc -W $^ -o $@
build-%: %.lexc.hfst
	@

%.twol.hfst: %.twol
	${hb}twolc $^ -o $@
build2-%: %.twol.hfst
	@

chv.gen.hfst: chv.lexc.hfst chv.twol.hfst
	${hb}compose-intersect -1 chv.lexc.hfst -2 chv.twol.hfst -o $@
compose-chv: chv.gen.hfst
	${hb}fst2strings $^
ava.gen.hfst: ava.lexc.hfst ava.twol.hfst
	${hb}invert ava.lexc.hfst | ${hb}compose-intersect -1 - -2 ava.twol.hfst | ${hb}invert -o $@
compose-ava: ava.gen.hfst
	${hb}fst2strings $^

%.mor.hfst: %.gen.hfst
	${hb}invert $^ -o $@

%.png: %.hfst
	${hb}minimise $^ | ${hb}fst2txt | python3 att2dot.py | dot -Tpng -o$@
graph-%: %.gen.png
	open $^
graphl-%: %.lexc.png
	open $^

string-%: %.lexc.hfst
	${hb}fst2strings -X obey-flags $^

txt-%: %.lexc.hfst
	${hb}fst2txt $^

total:=$(shell cat chv.crp.txt  | gsed 's/[^а-яӑӗăĕҫçА-ЯӐӖĂĔҪÇ]\+/ /g' | tr ' ' '\n'  | grep -v '^$$' | wc -l)
unknown:=$(shell cat chv.crp.txt  | gsed 's/[^а-яӑӗăĕҫçА-ЯӐӖĂĔҪÇ]\+/ /g' | tr ' ' '\n'  | grep -v '^$$' | ${hb}lookup -qp chv.mor.hfst  | grep 'inf' | wc -l)
coverage: chv.mor.hfst
	@python -c "print((${total}-${unknown})/${total}*100)"

paradigm: noun-paradigm.txt chv.gen.hfst
	cat noun-paradigm.txt | gsed "s/^/у р а м /g"  | ${hb}regexp2fst -j > uram.hfst
	${hb}compose-intersect -2 chv.gen.hfst -1 uram.hfst | ${hb}fst2strings

chv.gen_guesser.hfst: chv.stem.regex chv.lexc.hfst chv.twol.hfst
	echo "source chv.stem.regex\nsave stack chv.stem.hfst\nhyvästi" | ${hb}xfst
	${hb}substitute -i chv.lexc.hfst -o chv.lexc_guesser.hfst  -f '🂡:🂡' -T chv.stem.hfst
	${hb}compose-intersect -1 chv.lexc_guesser.hfst -2 chv.twol.hfst -o chv.gen_guesser.hfst
guesser: chv.gen_guesser.hfst
	echo "лайк<guess><n><pl><ins>" | ${hb}lookup -qp chv.gen_guesser.hfst 

restrict: chv.restrict.regex chv.gen_guesser.hfst
	${hb}regexp2fst chv.restrict.regex -o chv.restrict.hfst
	${hb}invert chv.gen_guesser.hfst | ${hb}compose -1 - -2 chv.restrict.hfst -o chv.mor_guesser.hfst
	echo "лайксемпе" | ${hb}lookup -qp chv.mor_guesser.hfst 

prob: chv.frq.txt chv.gen.hfst
	cat chv.frq.txt | python3 freq2prob.py | ${hb}strings2fst -j -o chv.surweights.hfst
	echo "?::0" | ${hb}regexp2fst | ${hb}repeat | ${hb}reweight -e -a 15.0 | ${hb}minimise -o chv.maxweight.hfst
	${hb}union -1 chv.surweights.hfst -2 chv.maxweight.hfst -o chv.weights.hfst
	${hb}compose -1 chv.gen.hfst -2 chv.weights.hfst -o chv.gen_weighted.hfst

clean:
	rm -f *.hfst *.png
