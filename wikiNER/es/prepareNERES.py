__author__ = 'oscarmarinmiro'

import os
import sys
from rdflib.graph import Graph
import pprint
import re
import json

sys.path.append('../lib')

from textOps import flattenWikipedia,cleanWikilink,cleanWikipedia

MIN_INLINKS = 20


ONTO_DELETE = False

LABELS_FILE = os.path.join("../data/DBPedia","labels_en_uris_es.nt")
LINKS_FILE = os.path.join("../data/wikiPedia","articles.links.es.tsv")
WIKICAT_FILE = os.path.join("../data/DBPedia","article_categories_en_uris_es.nt")
INSTANCE_FILE = os.path.join("../data/DBPedia","instance_types_en_uris_es.nt")
CAT_LABELS = os.path.join("../data/DBPedia","category_labels_en_uris_es.nt")
ARTICLE_CAT = os.path.join("../data/DBPedia","article_categories_en_uris_es.nt")
FORBIDDEN_PATTERNS = os.path.join("conf/es-forbidden-patterns.txt")

OUT_FILE = os.path.join("../data/DBPedia","es-article-parsed.json")
OUT_CAT_FILE = os.path.join("../data/DBPedia","es-cats-parsed.json")

#ALLOWED_INSTANCES = {'http://www.w3.org/2002/07/owl#Thing':1,'http://dbpedia.org/ontology/Organisation':1,'http://dbpedia.org/ontology/Person':1,'http://dbpedia.org/ontology/Place':1,'http://dbpedia.org/ontology/Website':1}

#ALLOWED_INSTANCES = {'http://dbpedia.org/ontology/Organisation':1,'http://dbpedia.org/ontology/Person':1,'http://dbpedia.org/ontology/Place':1,'http://dbpedia.org/ontology/Website':1}


def quickModTripletFromLine(line):
    matchObj = re.match( r'<(.*?)> <(.*?)> "(.*?)"', line)

    if matchObj:
        return (matchObj.group(1),matchObj.group(2),matchObj.group(3))
    else:
        return ""

def quickTripletFromLine(line):
    matchObj = re.match( r'<(.*?)> <(.*?)> <(.*?)>', line)

    if matchObj:
        return (matchObj.group(1),matchObj.group(2),matchObj.group(3))
    else:
        return ""


def getTripletFromLine(line):
    g = Graph()
    g.parse(data=line, format="nt")

    returnTriplet = ()

    for triplet in g:
        returnTriplet = triplet

    return returnTriplet


# Comprueba si el texto esta en la lista forList pasada de expresiones regulares prohibidas


def checkForbidden(text,forList):
    for expr in forList:
        if re.match(expr,text):
            return True
    return False

# Cargo los patrones prohibidos

forbiddenPatterns = []

print "Loading forbidden patterns"

fileIn = open(FORBIDDEN_PATTERNS,"rb")

for line in fileIn:
    line = line.rstrip().decode("utf8")
    forbiddenPatterns.append(line)
fileIn.close()

# Cargo los inlinks de la wikipedia (OJO, wikipedia)

tmpInlinks = {}

print "Loading wikipedia links..."

fileIn = open(LINKS_FILE,"rb")

count = 0

for line in fileIn:
    line = line.rstrip()
    (article,inlinks) = line.split("\t")

    try:
        if not checkForbidden(article.decode("utf8"),forbiddenPatterns):
            article = cleanWikilink(article.decode("utf8"))

            inlinks = int(inlinks)

            # OJO la segunda condicion es porque en el fichero se repiten articulos con inlinks decrecientes

            if inlinks > MIN_INLINKS and article not in tmpInlinks:
                tmpInlinks[article] = int(inlinks)
        else:
            print "El articulo %s no pasa el test de expresiones prohibidas" % article.decode("utf8")

    except:
        print "Error en la carga del articulo"

    if (count%10000) == 0:
        print count

    count+=1

print "After mininlink %d filtering, %d articles remain" % (MIN_INLINKS,len(tmpInlinks.keys()))

#pprint.pprint(tmpInlinks)

inlinksDict = {}

fileIn = open(LABELS_FILE,"rb")

canonicalNameDict = {}

count = 0
casque = 0
testDict = {}

for line in fileIn:

    triplet = quickModTripletFromLine(line.rstrip())

    if len(triplet)>0:

        try:
            canonicalName = triplet[0]        
            languageName = triplet[2].decode('unicode-escape')

            if languageName in tmpInlinks:
                canonicalNameDict[canonicalName] = {}
                canonicalNameDict[canonicalName]['inlinks'] = tmpInlinks[languageName]
                canonicalNameDict[canonicalName]['langOriginal'] = languageName
                canonicalNameDict[canonicalName]['langFlat'] = flattenWikipedia(cleanWikipedia(languageName))
                canonicalNameDict[canonicalName]['ontoEntities'] = []
                canonicalNameDict[canonicalName]['categories'] = []                
                testDict[languageName] = 1

                if canonicalName not in inlinksDict:
                    inlinksDict[canonicalName] = 1
                inlinksDict[canonicalName]+=1

        except:
            print "Error en la carga de entrada DBPedia"
            casque+=1

        if count%100000 == 0:
            print count

        count+=1

fileIn.close()

print "Hay %d casques" % casque

fuera = 0

for article in tmpInlinks:
    if article not in testDict:
        print "===== El articulo %s no esta en los canonicos y tiene inlinks %d ====" % (article.encode("utf8"),tmpInlinks[article])
        fuera+=1

print "Se quedan fuera: %d" % fuera

numEntries = len(canonicalNameDict.keys())

print "Numero de entradas despues de inlinks cruce con wikipedia: %d" % numEntries

print "Filtrando por ontologia"

# ONTOLOGY FILTER

instancesDict = {}

fileIn = open(INSTANCE_FILE,"rb")
count = 0
for line in fileIn:
    triplet = quickTripletFromLine(line.rstrip())
    if len(triplet)>0:
        canonicalName = triplet[0]
        instanceType = triplet[2]
        if canonicalName in canonicalNameDict:
#            if instanceType in ALLOWED_INSTANCES:
            canonicalNameDict[canonicalName]['ontoEntities'].append(instanceType)

    count+=1
    if (count%100000) == 0:
        print count

fileIn.close()


# Eliminar de canonicalNameDict las que tengan len 0 en instancesDict

if ONTO_DELETE:
    toDelete = {}

    for canonicalName in canonicalNameDict:
        if len(canonicalNameDict[canonicalName]['ontoEntities'])==0:
            toDelete[canonicalName] = 1

    print "Voy a borrar por no tener ontologia %d articulos" % len(toDelete.keys())

    for canonicalName in toDelete:
        del(canonicalNameDict[canonicalName])

numEntries = len(canonicalNameDict.keys())

print "Numero de entradas filtradas por ontologia: %d" % numEntries

print "Traducciones de categorias"

canonicalCatDict = {}

fileIn = open(CAT_LABELS,"rb")
count = 0
for line in fileIn:
    triplet = quickModTripletFromLine(line.rstrip())
    if len(triplet)>0:
        canonicalName = triplet[0]
        langName = triplet[2]
        try:
            canonicalCatDict[canonicalName] = langName.decode('unicode-escape')
        except:
            print "Casque en codificacion categoria"

    count+=1

    if (count%100000) == 0:
        print count

fileIn.close()



print "Anyadiendo info de categoria"

catsDict = {}

fileIn = open(ARTICLE_CAT,"rb")
count = 0
for line in fileIn:
    triplet = quickTripletFromLine(line.rstrip())
    if len(triplet)>0:
        canonicalName = triplet[0]
        canonicalCategory = triplet[2]

        if canonicalName in canonicalNameDict:
            if canonicalName not in catsDict:
                canonicalNameDict[canonicalName]['categories'].append(canonicalCategory)

    count+=1

    if (count%100000) == 0:
        print count

fileIn.close()

print "Numero de entradas finales %s" % len(canonicalNameDict.keys())



#pprint.pprint(canonicalNameDict)

print "======================="

#pprint.pprint(canonicalCatDict)

print "Dumping articles file..."

fileOut = open(OUT_FILE,"wb")

json.dump(canonicalNameDict,fileOut,indent=4)

fileOut.close()

print "Dumping cat translation file..."

fileCats = open(OUT_CAT_FILE,"wb")

json.dump(canonicalCatDict,fileCats,indent=4)

fileCats.close()
