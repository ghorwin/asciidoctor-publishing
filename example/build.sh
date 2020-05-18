#!/bin/bash

cd ./de &&

echo '*** Generating html ***' &&
python ../../scripts/adoc-image-prep.py html . &&
asciidoctor main.adoc &&

echo '*** Generating pdf ***' &&
python ../../scripts/adoc-image-prep.py pdf . &&
asciidoctor-pdf -a pdf-theme=pdf-theme.yml -r ./rouge_theme.rb -a pdf-fontsdir="./fonts;GEM_FONTS_DIR" main.adoc &&

# reset to html type
python ../../scripts/adoc-image-prep.py html . &&

cd -

