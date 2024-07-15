article_name=responsive_latex_hoftich
tex_file=$(article_name).tex
pdf_file=$(article_name).pdf
build_dir=hoftich_responsive
zip_file=$(build_dir).zip
source_files=$(tex_file) $(pdf_file) Makefile responsive.bib 

presentation_source=presentation-text.tex bio.tex
handout_name = responsive_handout
handout_source = $(handout_name).tex
handout_pdf = $(handout_name).pdf

slides_name = responsive_presentation
slides_source = $(slides_name).tex
slides_pdf = $(slides_name).pdf

All: $(slides_pdf) $(handout_pdf) $(pdf_file)

$(slides_pdf): $(slides_source) $(presentation_source)
	lualatex $<

$(handout_pdf): $(handout_source) $(presentation_source)
	lualatex $<


$(pdf_file): $(tex_file)
	lualatex $<
	bibtex $(article_name)
	lualatex $<



build: $(pdf_file)
	rm -rf $(build_dir) $(zip_file)
	mkdir $(build_dir)
	cp $(source_files) $(build_dir)
	cp `kpsewhich responsive.sty` $(build_dir)
	cp -r img/ $(build_dir)
	zip -r $(zip_file) $(build_dir)

