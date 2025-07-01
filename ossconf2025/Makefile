
sources := hoftich-handout.tex hoftich-slides.tex presentation.tex

ALL: hoftich-slides.pdf index.html

hoftich-slides.pdf: $(sources)
	lualatex hoftich-slides.tex

index.html: $(sources)
	make4ht -c config.cfg -lj ossconf2025 -a debug $<
