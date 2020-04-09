import csv
from nltk.corpus import wordnet as wn
from nltk.corpus import brown
from nltk.stem.wordnet import WordNetLemmatizer

#manually set intensity of often-used adverbs
i1 = ['very','highly','truly','really','quite']
i2 = ['extremely','exceedingly','super','passing','remarkably']



class Capture: #Object for saving intensity-adverb, and modified wordm and it's position relative to adverb
    def __init__(self,adverb,position,word):
        self.adverb = adverb
        self.position = position
        self.word = word

class Store: #bject for Store the Captures
    def __init__(self):
        self.adjective = {}
        self.adverb = {}
        self.verb = {}

def is_be_verb(syn): # check wheter it's original form is "be" or not
    if 'be' is WordNetLemmatizer().lemmatize(syn,'v'):
        return True
    else :
        return False


def is_sign(syn): #check whether it is symbol or not
    if syn in [',','.','``']:
        return True
    else:
        return False


def store_word(store,sentence,current,position,intensity):  #handle for three cases and pass it to "save" function
    target = sentence[current+position]
    syns = wn.synsets(target)
    if position == -1 and current >1 and is_be_verb(sentence[current-2]): # for the case like "he is praise highly" , "be" is located two step previous than adverb
        for s in syns:
            if not is_sign(target) and not s.pos() == 'n':
                save(store,s,Capture(sentence[current],position,target),intensity)

    elif position == 1: # for the next word
        if sentence[current+position] in ['being','been''doing'] and current+2<len(sentence): # case for "being" and "been"  like he is really being good
            for s in wn.synsets(sentence[current+position+1]):
                if not is_sign(target) and not s.pos() == 'n':
                    save(store, s, Capture(sentence[current], position, sentence[current+position+1]), intensity)

        elif not is_be_verb(sentence[current+position]): ### normal cases, "he had been highly praised."
            for s in syns:
                if not is_sign(target) and not s.pos() == 'n':
                    save(store, s, Capture(sentence[current], position, target), intensity)

def save(store,synset,word,intensity):  #put the inputs to proper dictionary by pos()
    pos = synset.pos()
    if pos == 'a': #for adjective
        increase(store.adjective,synset,word,intensity)
    elif pos == 'v': #for verb
        increase(store.verb,synset,word,intensity)
    elif pos == 'r': #for adverb
        increase(store.adverb, synset,word,intensity)

def increase(dict,synset,word,intensity): #increase the count by its intensity
    if synset in dict.keys():
        dict[synset][1] = dict[synset][1] +intensity
    else:
        dict[synset] = [word,intensity]


"""----------------------------Counting_Freq --------------------------------"""
store = Store()
sents = brown.sents(categories = ['news','humor', 'editorial','science_fiction']) #input nltk corpora

for s in sents:
    for i in range(len(s)): #for each sentencs, check there's intensity adverb or not
        if s[i].lower() in i1:  # for the adverb group i1.
            if 2 <= i and is_be_verb(s[i-2]): #check and store the neighbor words.
                store_word(store,s,i,-1,1)
            if i < len(s) - 1:
                store_word(store,s,i, 1, 1)
        if s[i].lower() in i2:# for the adverb group i2.
            if 2 <= i and is_be_verb(s[i-2]):
                store_word(store,s,i, -1, 2)
            if i < len(s) - 1:
                store_word(store,s,i,1, 2)


"""----------------------------Comparing Freq------------------------------"""

def compare_freq(result,dict): #compare the summation of accumulated intensity.
    lst = list(dict.keys())
    for i in range(len(lst)):
        syn1 = lst[i]
        cap1 = dict[syn1][0] #capture of 1nd iter

        for j in range(i+1,len(lst)):
            syn2 = lst[j]
            cap2 = dict[syn2][0] #capture of 2nd iter
            if cap1.word == cap2.word:
                continue

            similarity = wn.wup_similarity(syn1, syn2) #get similarity
            if syn1.pos() == syn2.pos() and similarity is not None and similarity >0.7:
                if dict[syn1][1]>dict[syn2][1]:  #make triples
                    result.append(make_triple(cap2.word,cap1))
                else:
                    result.append(make_triple(cap1.word,cap2))

def make_triple(cap_strong,cap_weak): #make triple for outuput
    if cap_weak.position == -1:
        return (cap_strong,cap_weak.word,cap_weak.adverb)
    else:
        return (cap_strong,cap_weak.adverb,cap_weak.word)

result = []
compare_freq(result,store.adverb)
compare_freq(result,store.adjective)
compare_freq(result,store.verb)


f = open('CS372_HW1_output_20170221.csv','w',newline='')
wr = csv.writer(f)
wr.writerow(result[:50])
f.close()


