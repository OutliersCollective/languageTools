languageTools
=============

Collection of language analysis and processing tools for spanish language

FRIENDLY WARNING: 
This is a work in progress, there will be *HUGE* updates from 17th June 2013 until 15th July 2013.

After that date, the first beta of these tools will be released, including:
  - A Named Entity Recognition/Classification library based on DBPedia and Wikipedia data
  - A text categorization customizable module
  - A sentiment analysis module at the entity level
  - A mood detection module
  - (Probably) A context detection module and entity disambiguation method based on that module

Below we will be posting updates. At 15th July 2013, this public repository will undertake a whole revamp, and will be
released as an automated python module (i.e: no installation hassles and the like)

============================

UPDATE (17th June 2013): NER/NEC Code added.

You can test it by cloning this repository. At the moment no building from Wikipedia and DBPedia is provided, but
the needed files to run it are on the 'data' and 'wikiNER/conf' directories.

The module implementing the NER/NEC is on 'wikiNER/es/NerES.py' with an example on how to run it on lines 331-353

Dependencies: *None*. The module runs on standard python modules

Tested on: Python 2.6/2.7 [Not python 3 compatible], on Debian and MacOSX systems

Please keep in mind that NerES.py must be ran from 'wikiNER' directory like this: 'python es/NerES.py'

You can play with an online demo on this front-end (in spanish): http://assets.outliers.es:8998/

