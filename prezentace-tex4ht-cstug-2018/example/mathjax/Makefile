all: simple.html mathml-test.html mathml-mathjax.html mathjax.html

simple.html: simple.tex content.tex
	make4ht -um draft simple svg

mathml-test.html: mathml-test.tex content.tex
	make4ht -um draft $< mathml
	
mathml-mathjax.html: mathml-mathjax.tex content.tex
	make4ht -um draft $< "mathjax,mathml"

mathjax.html: mathjax.tex content.tex
	make4ht -um draft $< "mathjax"
