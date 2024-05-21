article_name=responsive_latex_hoftich
tex_file=$(article_name).tex
pdf_file=$(article_name).pdf
build_dir=hoftich_responsive
zip_file=$(build_dir).zip
source_files=$(tex_file) $(pdf_file) Makefile responsive.bib 

$(pdf_file): $(tex_file)
	lualatex $<
	biber $(article_name)
	lualatex $<



build: $(pdf_file)
	rm -rf $(build_dir) $(zip_file)
	mkdir $(build_dir)
	cp $(source_files) $(build_dir)
	cp `kpsewhich responsive.sty` $(build_dir)
	cp -r img/ $(build_dir)
	zip -r $(zip_file) $(build_dir)

