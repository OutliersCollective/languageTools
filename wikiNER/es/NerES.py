__author__ = 'oscarmarinmiro'
# -*- coding: utf8 -*-

import os
import sys
import pprint
import json

import time

sys.path.append('../lib')

from textOps import flattenNERInputEs

#ALLOWED_INSTANCES = ['http://dbpedia.org/ontology/Organisation','http://dbpedia.org/ontology/Person','http://dbpedia.org/ontology/Place','http://dbpedia.org/ontology/Website']


IN_FILE = os.path.join("../data/DBPedia","es-article-parsed.json")
IN_CAT_FILE = os.path.join("../data/DBPedia","es-cats-parsed.json")
IN_STOPWORDS_FILE = os.path.join("../data/langModel","es-stopwords.txt")
IN_SEPARATORS_FILE = os.path.join("../data/langModel","es-separators.txt")
IN_CONTEXTS_DIR = os.path.join("conf/es-contexts")

ALL_CONTEXT = "all"

CONTEXT_FILE_NAME = "contextData.json"

#TODO: Hacer frontal

class NEREs:

    def __init__(self):

        print "Initializing NER..."

        # Loading stopwords

        print "Loading stopwords..."

        self.stopwords = {}

        fileIn = open(IN_STOPWORDS_FILE,"rb")

        for line in fileIn:
            word = line.rstrip().decode("utf8").lower()
            self.stopwords[word] = True

        fileIn.close()

        print "Loading separators..."

        # Loading separators

        self.separators = {}

        fileIn = open(IN_SEPARATORS_FILE,"rb")

        for line in fileIn:
            separator = line.rstrip("\n").decode("utf8")
            self.separators[separator] = True

        fileIn.close()

        # Load contexts

        self.myContexts = {}

        print "Loading spanish contexts"

        for name in os.listdir(IN_CONTEXTS_DIR):
            if os.path.isdir(os.path.join(IN_CONTEXTS_DIR,name)):

                contextName = name

                self.myContexts[contextName] = {}
                self.myContexts[contextName]['forbiddenEntities'] = {}
                self.myContexts[contextName]['forbiddenCat'] = {}
                self.myContexts[contextName]['addedEntities'] = {}

                print "Cargando contexto %s" % contextName

                fileIn = open(os.path.join(IN_CONTEXTS_DIR,contextName,CONTEXT_FILE_NAME),"rb")

                cStruct = json.load(fileIn,"utf8")

                pprint.pprint(cStruct)

                for entry in cStruct['forbiddenCat']:
                    self.myContexts[contextName]['forbiddenCat'][entry] = True

                for entry in cStruct['forbiddenEntities']:
                    self.myContexts[contextName]['forbiddenEntities'][entry] = True

                for entry in cStruct['addedEntities']:
                    self.myContexts[contextName]['addedEntities'][entry['langFlat']] = entry

        # And now, propagate the 'all' context to other contexts [only if keys does not exist...]

        for context in self.myContexts:
            if context!= ALL_CONTEXT:
                for key in ['addedEntities','forbiddenEntities','forbiddenCat']:
                    for entry in self.myContexts[ALL_CONTEXT][key]:
                        if entry not in self.myContexts[context][key]:
                            self.myContexts[context][key][entry] = self.myContexts[ALL_CONTEXT][key][entry]


        # Final contexts nice printing for debugging purposes

        pprint.pprint(self.myContexts)

        # load articles-entities file

        print "Loading DBPedia articles..."

        fileIn = open(IN_FILE,"rb")

        self.articles = json.load(fileIn)

        fileIn.close()

        # load category spanish translation

        print "Loading category translation..."

        fileIn = open(IN_CAT_FILE,"rb")

        self.categories = json.load(fileIn)

        fileIn.close()

        self.entities = {}

        # self.entitied dictionary contains all entries by langFlat.
        # In case of collision, several entries are added as a list

        for article in self.articles.keys():
            self.articles[article]['canonical'] = article
            text = self.articles[article]['langFlat']
            if text not in self.entities:
                self.entities[text] = []
            self.entities[text].append(self.articles[article])

        # Sort collisions by inlinks

        for text in self.entities:
            sortedArticles = sorted(self.entities[text],key = lambda entity: entity['inlinks'],reverse=True)
            self.entities[text] = sortedArticles

        print "NER initialized..."


    # Check if an entry has a category in forbiddenCat for a context

    def forbiddenCategory(self,entry,context):
        for category in entry['categories']:
            if category in self.myContexts[context]['forbiddenCat']:
                return True
        return False

    # Get all article matches for line passed (can be a multiline because '\t' and '\n' are translated)
    # Only include if inlinks >limit

    def getAllSequences(self,line,limit,context):
        sequences = []
        line = " "+line+" "
        for i in range(0,len(line)-1):
            for j in range(i+1,len(line)):
                if line[i] in self.separators and line[j] in self.separators:
                    seq = line[i+1:j]
                    # If sequence not in stopwords
                    if seq not in self.stopwords:

                        # For each entry... filter by inlink

                        finalEntries = []

                        # If sequence in context added Entities
                        # (keep in mind there must be only one entry by definition...

                        if seq in self.myContexts[context]['addedEntities']:
                            entry = self.myContexts[context]['addedEntities'][seq]
                            # Check inlinks of entry
                            if not entry['inlinks']<limit and not self.forbiddenCategory(entry,context):
                                finalEntries.append(entry)

                        else:
                            if seq in self.entities:

                                # Check entry in context

                                for entry in self.entities[seq]:
                                    # Check if inlinks of entry > limit and entry not in forbidden (context-dependent)
                                    if not entry['inlinks']<limit and not entry['canonical'] in self.myContexts[context]['forbiddenEntities'] and not self.forbiddenCategory(entry,context):
                                        finalEntries.append(entry)

                        # If there are entries ===> append

                        if len(finalEntries) > 0:
                            # LOOKOUT!! As we added a beginning " ", begin and end is i and j-1
                            # [regarding original text]a
                            sequences.append({'text':seq,'begin': i,'end': j-1,'value':finalEntries})
        return sequences

    # Build a dict: key==> string position; value ==> all matches for that position (overlapping matches)

    def overlapSequences(self,sequences):
        overlap = {}
        count = 0
        for seq in sequences:
            entryCount = 0
            for entry in seq['value']:
                for i in range(seq['begin'],seq['end']):
                    if i not in overlap:
                        overlap[i] = []
                    overlap[i].append([count,entryCount])
                entryCount += 1
            count += 1
        return overlap

    # Aux sort function to get only the first overlap in removeOverlaps (below)
    def overSort(self,entry,sequences):
        return sequences[entry[0]]['end']-sequences[entry[0]]['begin']

    # Remove the overlaps in list of matches (sequences structure)

    def removeOverlaps(self,overDict,sequences):
        removeIndexes = {}
        finalSequences = []
        for i in overDict:
            # If more than one entry for this string position
            if len(overDict[i])>1:
                # sort
                best = sorted(overDict[i], key = lambda entry: self.overSort(entry,sequences),reverse=True)
                # make a dict for every removable match (note that the dict has 2 'dimensions': first is the position, second is the overlap index
                # for that position
                for notBest in best[1:]:
                    if notBest[0] not in removeIndexes:
                        removeIndexes[notBest[0]] = {}
                    removeIndexes[notBest[0]][notBest[1]] = 1

        # Make a copy of sequences, removing overlaps
        for i in range(0,len(sequences)):
            finalSequences.append({'begin':sequences[i]['begin'],'end':sequences[i]['end'],'text':sequences[i]['text'],'value':[]})
            for j in range(0,len(sequences[i]['value'])):
                # If overlap index not in removeIndexes ==> add
                if not (i in removeIndexes and j in removeIndexes[i]):
                    finalSequences[i]['value'].append(sequences[i]['value'][j])

        # Finally remove positions that are now 'empty'

        returnSequences = []

        for i in range(0,len(finalSequences)):
            if len(finalSequences[i]['value'])>0:
                returnSequences.append(finalSequences[i])

        return returnSequences

    # Split sequences into 'concept' and 'entity'. Also filter out ontoEntries not present
    # in allowedInstances (for 'type' entry only)
    def splitAndFilter(self,sequences,allowedInstances,text):

        # Insert allowed instance type in a dict for fast lookup
        allowedDict = {}
        for type in allowedInstances:
            allowedDict[type] = True

        # Final structure
        finalData = {}
        finalData['concepts'] = []
        finalData['entities'] = []

        # For every entry insert in 'concepts' or 'entities' subentry

        for entry in sequences:
            newEntry = {}
            newEntry['begin'] = entry['begin']
            newEntry['end'] = entry['end']
            newEntry['canonical'] = entry['value'][0]['canonical']
            newEntry['categories'] = entry['value'][0]['categories']
            newEntry['inlinks'] = entry['value'][0]['inlinks']
            newEntry['DBPediaText'] = entry['value'][0]['langOriginal']
            newEntry['match'] = text[entry['begin']:entry['end']]
            # If no ontoEntities ==> concept
            if len(entry['value'][0]['ontoEntities'])!=0:
                # If entity, only insert in type desired entities
                newEntry['ontoEntries'] = entry['value'][0]['ontoEntities']
                newEntry['type'] = []
                for type in entry['value'][0]['ontoEntities']:
                    if type in allowedDict:
                        newEntry['type'].append(type)
                finalData['entities'].append(newEntry)
            else:
                finalData['concepts'].append(newEntry)

        return finalData

    def doNER(self,text,limit,allowedInstances,context="all"):

        # Translate text

        newText = flattenNERInputEs(text.lower())

        # Get all matches

        seq = self.getAllSequences(newText,limit,context)

        # Get overlap structure

        overlap = self.overlapSequences(seq)

        # Remove overlap based on overSort criteria and return final matches (with overlap removed)

        finalSequences = self.removeOverlaps(overlap,seq)

        # Nice formating of finalSequences

        finalData = self.splitAndFilter(finalSequences, allowedInstances, text)

        finalData['query'] = {}

        finalData['query']['text'] = text
        finalData['query']['limit'] = limit
        finalData['query']['context'] = context

        return finalData


if __name__ == '__main__':

    print "Beginning test..."

    ALLOWED_INSTANCES = ['http://dbpedia.org/ontology/Organisation','http://dbpedia.org/ontology/Person','http://dbpedia.org/ontology/Place','http://dbpedia.org/ontology/Website']

    originalText = "en la puerta.del sol me voy al.báRcelona sPortig club y en mAdrid y en tArragona con marianO rajoY en voDafOne".decode("utf8")

    myNER = NEREs()

    initTime = time.time()

    finalData = []

    for i in range(0,1000):
        finalData = myNER.doNER(originalText, 50, ALLOWED_INSTANCES)

    elapsed = time.time() -initTime


    print "=========================="

    pprint.pprint(finalData)

    print "Elapsed time for 1000 iterations = %f" % elapsed


