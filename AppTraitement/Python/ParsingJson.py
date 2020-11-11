import json     # json_decode
import re       # preg_match

class ParsingJson:
    jsonFile = ""
    jsonArray = {}
    bidenTweetArray = {}
    trumpTweetArray = {}

# Constructor
    def __init__(self, f):
        self.jsonFile = f
        self.jsonArray = {}
        self.bidenTweetArray = {}
        self.trumpTweetArray = {}



# ------------------ Traitement File Entrée ------------------
    # Récupère le json et le transforme en tableau
    def getJsonToArray(self, i = 0):
        with open(self.jsonFile) as f:
            for value in json.load(f):
                self.jsonArray[i] = json.loads(value)
                i += 1



# ------------------ Séparation Trump / Biden ------------------

    # Find si tweet talk about T or B
    def findTrumpOrBiden(self):
        patternBiden = r"@?(joe)?(\s)?biden | @?biden(\s)?(joe)?"
        patternTrump = r"@?(donald)?(\s)?trump | @?trump(\s)?(donald)?"
        for key, value in self.jsonArray.items():
            if re.search(patternTrump, value['text'], re.IGNORECASE | re.MULTILINE):
                self.trumpTweetArray[key] = value
            if re.search(patternBiden, value['text'], re.IGNORECASE | re.MULTILINE):
                self.bidenTweetArray[key] = value

    # Return array with Trump message
    def getTrumpArray(self):
        return self.trumpTweetArray

    # Return array with Biden message
    def getBidenArray(self):
        return self.bidenTweetArray



# ------------------ Suppression Symbols ------------------

    # Extract important word
    def extractionSymbols(self, array):
        arrayWithoutSymbols = {}
        pattern = r"@|&|'|\"|\||\(|\)|<|>|#|\.|\,|\/|\?|\!|\;|\:|\\|\n||-|_|[1234567890]*|(\s[abcdefghijklmnopqrstuvwxyz]\s)"
        for key, value in array.items():
            arrayWithoutSymbols[key] = re.sub(pattern, "", value['text'])
        return arrayWithoutSymbols



# ------------------ Count Occurence Word ------------------

    # Explode String to Char Array
    def traitementWord(self, string):
        return string.lower().split(' ')

    # Count number of occurence word
    def countOccurenceWord(self, array):
        arrayCountOccurence = {"word" : 1}
        for key, value in array.items():
            for word in self.traitementWord(value):
                if word in arrayCountOccurence:
                    arrayCountOccurence[word] += 1
                else:
                    arrayCountOccurence[word] = 1
        return arrayCountOccurence



# ------------------ Array Sorted ------------------

    def arraySorted(self, array):
        arraySorted = {}
        for key, value in sorted(array.items(), key = lambda x: x[1], reverse = True):
            arraySorted[key] = value
        return arraySorted



# ------------------ First Elems Array ------------------

    def getFirstElemsArray(self, array, stopValue, stop = 0):
        arrayFirstElem = {}
        for key, value in array.items():
            if not key:
                stop -= 1
            else:
                arrayFirstElem[key] = value
                stop +=1
                if stop == stopValue:
                    break

        return arrayFirstElem



# ------------------ Traitement File Sortie ------------------

    # Fichier json contenant les résultat
    def createResultFile(self, name, data):
        with open('AppTraitement/Result/' + name + '.json', "w") as filout:
            filout.write(json.dumps(data))









#
