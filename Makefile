.PHONY: all pdf clean

all: pdf

pdf:
	cd submission && latexmk -pdf -pdflatex='pdflatex -shell-escape -synctex=1 -interaction=nonstopmode -file-line-error' main.tex

clean:
	cd submission && latexmk -CA
