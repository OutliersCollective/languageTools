__author__ = 'oscarmarinmiro'
# -*- coding: utf8 -*-

import os
import sys
import re

# Paso del sql a un tsv con 'articulo\tinlinks'

print "Ingiriendo " + sys.argv[1] + "..."

fileIn = open(sys.argv[1],"r")

articleDict = {}

for line in fileIn:
    line = line.rstrip()

    # Compruebo que es una linea con SQL-values

    if re.match(r'INSERT INTO',line) is not None:
        # LA expresion regular
        expression = r"\(.*?,.*?,'(.*?)'\)"
        
        matches = re.finditer(expression,line)

        for match in matches:
            article = match.group(1)

            if article not in articleDict:
                articleDict[article] = 1
            else:
                articleDict[article]+=1


fileIn.close()

# Cuando acabo: ordeno

print "Ordenando: " + str(len(articleDict.keys()))

sortedArticles = sorted(articleDict.keys(), key = lambda article: articleDict[article], reverse = True)

fileOut = open(sys.argv[2],"w")

for article in sortedArticles:
    fileOut.write("\t".join([article,str(articleDict[article])])+"\n")

fileOut.close()
