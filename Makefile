.PHONY: asiaccs.pdf all clean clean-build

all: main.pdf

%.tex: %.raw
	./raw2tex $< > $@

%.tex: %.dat
	./dat2tex $< > $@

main.pdf: main.tex
	latexmk -C && latexmk -pdf -pdflatex="pdflatex -shell-escape -synctex=1 -interaction=nonstopmode -file-line-error" main.tex

# Compile and automatically clean intermediate files after successful build
clean-build:
	latexmk -C && latexmk -pdf -pdflatex="pdflatex -shell-escape -synctex=1 -interaction=nonstopmode -file-line-error" main.tex && latexmk -c

clean:
	latexmk -CA
