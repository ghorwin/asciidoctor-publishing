# asciidoctor-publishing
Python scripts to assist with publishing Asciidoctor based documents using customized html and pdf outputs


## Overview

[Asciidoctor](https://asciidoctor.org) is an awesome publishing system, especially for technical documentation. It generates nice html-output and together with [asciidoctor-pdf](https://asciidoctor.org/docs/asciidoctor-pdf) also very nice pdf output.

Setting up the tool chain may be a bit tricky, so I summarized the steps to install it below (mostly for my own reference). Of course, (other) instructions can be found anywhere in the net.


### Image-related handling pdf and html output

With newer versions of asciidoctor-pdf, the style configuration is already very good (see example in this repository). However, there are some things that need to be handled differently in pdf-output and html-output. 
This mostly applies to image handling.

When viewing the html-documentation on the screen, most viewers will have a FullHD resolution and a content area with of about 700..800 px. Screenshots/images/pictures that are larger than this width will be automatically 
resized to fit the content width. This may be problematic for two reasons:

- the resizing algorithm in the web browser is usually not as good as in image processing software (see (Gimp)[https://www.gimp.org] an similar)
- sometimes, the image should not span the entire width for layouting purposes (but rather 80%). While this can be configured in the asciidoctor `image::` tag, still the webbrowser-based resizing may be problematic. See for yourself in 
the following examples

Image resizes in webbrowser:

![Image resized in webbrowser](images/diagram_examples/multichart_view_de-print.png =700x)

Image resized manually in graphics software:

![Image resized manually](images/diagram_examples/multichart_view_de.png)



## Installation/tool chain setup

### Linux/Ubuntu

```bash
> sudo apt install asciidoctor 

# Install ruby, and then:

> sudo gem install asciidoctor-pdf --pre
> sudo gem install rouge

# Install rouge syntax highlighter extension
> sudo gem install asciidoctor-rouge
> sudo gem install asciidoctor-mathematical
```





