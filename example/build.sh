#!/bin/bash

cd ./de &&

echo '*** Preparing html ***' &&
python ../../scripts/adoc-image-prep.py html . &&
echo '*** Generating html ***' &&
asciidoctor main.adoc &&

echo '*** Preparing pdf ***' &&
python ../../scripts/adoc-image-prep.py pdf . &&
echo '*** Generating pdf ***' &&
asciidoctor-pdf -a pdf-theme=pdf-theme.yml -r ./rouge_theme.rb -a pdf-fontsdir="./fonts;GEM_FONTS_DIR" main.adoc &&

# reset to html type
echo '*** Preparing html ***' &&
python ../../scripts/adoc-image-prep.py html . &&

cd -

