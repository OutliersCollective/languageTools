__author__ = 'oscarmarinmiro'
# -*- coding: utf8 -*-

import os
import sys
import re
import pprint
import traceback

sys.path.append('../../')

# Carga el tsv de inlinks y mete un campo nuevo con el nombre limpio y normalizado

from lib.textOps import okNameWikipedia,flattenWikipedia,cleanWikipedia

print "Ingiriendo " + sys.argv[1] + "..."

fileIn = open(sys.argv[1],"r")
fileOut = open(sys.argv[2],"w")

articleDict = {}

for line in fileIn:
    try:
        line = line.decode("utf-8").rstrip()

        (name, links) = line.split("\t")

        if okNameWikipedia(name):
            clean = cleanWikipedia(name)
            flatted = flattenWikipedia(clean)
            fileOut.write(("\t".join([clean,flatted,links])+"\n").encode("utf-8"))
    except:
        print "Casco en la linea" + pprint.pformat(line)
        traceback.print_exc()

fileIn.close()
fileOut.close()

