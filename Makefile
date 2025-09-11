.PHONY: asiaccs.pdf all clean

all: main.pdf

%.tex: %.raw
	./raw2tex $< > $@

%.tex: %.dat
	./dat2tex $< > $@

main.pdf: main.tex
	latexmk -pdf -pdflatex="pdflatex -shell-escape -interaction=nonstopmode" -use-make main.tex -f

clean:
	latexmk -CA
