from config import *


english_words = {}

def loadPPDB(ppdbFileName = \
            'Resources/ppdb-1.0-xxxl-lexical.extended.synonyms.uniquepairs'):

    global ppdbSim
    global ppdbDict

    count = 0
    
    ppdbFile = open(ppdbFileName, 'r')
    for line in ppdbFile:
        if line == '\n':
            continue
        tokens = line.split()
        tokens[1] = tokens[1].strip()
        ppdbDict[(tokens[0], tokens[1])] = ppdbSim
        count += 1




def presentInPPDB(word1, word2):

    global ppdbDict

    if (word1.lower(), word2.lower()) in ppdbDict:
        return True
    if (word2.lower(), word1.lower()) in ppdbDict:
        return True
    

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
 
    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)
 
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
 
    return previous_row[-1]



def wordRelatedness(word1, pos1, word2, pos2):

    global english_words
    global stemmer
    global ppdbSim
    global punctuations

    if english_words == {}:
        for line in open('english_words.txt', 'r'):
            word = line.strip()
            english_words[word] = 1

    if len(word1) > 1:
        canonicalWord1 = word1.replace('.', '')
        canonicalWord1 = canonicalWord1.replace('-', '')
        canonicalWord1 = canonicalWord1.replace(',', '')
    else:
        canonicalWord1 = word1
        
    if len(word2) > 1:
        canonicalWord2 = word2.replace('.', '')
        canonicalWord2 = canonicalWord2.replace('-', '')
        canonicalWord2 = canonicalWord2.replace(',', '')
    else:
        canonicalWord2 = word2
    
    
    if canonicalWord1.lower() == canonicalWord2.lower():
        return 1

    if stemmer.stem(word1).lower() == stemmer.stem(word2).lower():
        return 1

    if canonicalWord1.isdigit() and canonicalWord2.isdigit() and canonicalWord1 <> canonicalWord2:
        return 0

    if pos1.lower() == 'cd' and pos2.lower() == 'cd' and (not canonicalWord1.isdigit() and not canonicalWord2.isdigit()) and canonicalWord1 <> canonicalWord2:
        return 0

    # stopwords can be similar to only stopwords
    if (word1.lower() in stop_words and word2.lower() not in stop_words) or (word1.lower() not in stop_words and word2.lower() in stop_words):
        return 0

    # punctuations can only be either identical or totally dissimilar
    if word1 in punctuations or word2 in punctuations:
        return 0

    if presentInPPDB(word1.lower(), word2.lower()):
        return ppdbSim
    elif len(word1)>2 and len(word2)>2 and levenshtein(word1.lower(), word2.lower()) == 1 and (word1.lower() not in english_words or word2.lower() not in english_words):
        #print (word1, word2)
        return 1
    else:
        return 0




loadPPDB()

