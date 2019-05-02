common_tex=presentation-text.tex outline.tex
latex=lualatex

presentation=hoftich_bachotex_presentation
article= hoftich_tex4ht_bachotex_2019

all: handout.pdf handout.html  ${presentation}.pdf ${article}.pdf

handout.pdf: handout.tex  ${common_tex}
	$(latex) $<

handout.html: handout.tex ${common_tex}
	make4ht -ulm draft -c hej.cfg $<

blog:
	rm handout.published
	make4ht -ulm blog handout.tex


${presentation}.pdf: ${presentation}.tex ${common_tex}
	$(latex) $<

${article}.pdf: ${article}.tex
	$(latex) $<
