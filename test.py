import nltk
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer


i1 = ['very','highly','truly','really','real','quite']  #synset 형태로 바꿔주
i2 = ['highly','extremely','exceedingly','super','passing']

# for s in wn.synsets('good',('v','a','r')):
#     print(s,s.examples())
# al  = ['praise','rave','laud','tout','exalt']
# w=[]
# for a in al:
#     w.append(wn.synset(a.))
#     print(a)
#
# print(w)
#
# a = 'big'
# b = 'huge'
# q = wn.synsets(a,'a')[0]
# print(q)
# q2 = wn.synsets(b,'a')[0]
# print(q2)
#
# print(q.wup_similarity(q2))
# for a in al:
#     print(nltk.pos_tag(a))
#

for a1 in wn.synsets('extol'):
    for a2 in wn.synsets('praise'):
        print(a1.definition()," @@@",a2.definition())
        print(wn.wup_similarity(a1, a2))


#for a1 in wn.synsets('extol'):
    # for a2 in wn.synsets('praise'):
    #     print(wn.wup_similarity(wn.synsets('extol',a1.pos())[0], wn.synsets('praise')[0]))
# i1 = ['very','highly','truly','really','real','rattling']
# i2 = ['highly','extremely','exceedingly','super','passing']
# for i in i1:
#     print(i)
#     l = wn.synsets(i,'r')
#     for s in l:
#         print(s,s.definition())
#
# print(wn.lemmas('be'))
# print(WordNetLemmatizer().lemmatize('praised','v'))


import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import brown
from nltk.stem.wordnet import WordNetLemmatizer

i1 = ['very', 'highly', 'truly', 'really', 'quite']
i2 = ['extremely', 'exceedingly', 'super', 'passing', 'remarkably']


class Store:
    def __init__(self):
        self.adjective = {}
        self.adverb = {}
        self.verb = {}


class Capture:
    def __init__(self, adverb, position, word):
        self.adverb = adverb
        self.position = position
        self.word = word


class Result:
    def __init__(self):
        self.adjective = []
        self.adverb = []
        self.verb = []


def is_be_verb(syn):
    if 'be' is WordNetLemmatizer().lemmatize(syn, 'v'):
        return True
    else:
        return False


def is_sign(syn):
    if syn in [',', '.', '``']:
        return True
    else:
        return False


def store_word(store, adverb, position, word, intensity):
    syns = wn.synsets(word)
    for s in syns:

        if not is_be_verb(word) and not is_sign(word) and not s.pos == 'n':
            save(store, s, Capture(adverb, position, word), intensity)


def save(store, synset, word, intensity):
    pos = synset.pos()
    if pos == 'a':
        increase(store.adjective, synset, word, intensity)
    elif pos == 'v':
        increase(store.verb, synset, word, intensity)
    elif pos == 'r':
        increase(store.adverb, synset, word, intensity)


def increase(dict, synset, word, intensity):
    if synset in dict.keys():
        dict[synset][1] = dict[synset][1] + intensity
    else:
        dict[synset] = [word, intensity]


"""----------------------------Counting_Freq --------------------------------"""
store = Store()
sents = brown.sents(categories='news')

for s in sents:
    for i in range(len(s)):
        if s[i].lower() in i1:
            if 2 <= i and is_be_verb(s[i - 2]):
                store_word(store, s[i], 0, s[i - 1], 1)
            if i < len(s) - 1:
                store_word(store, s[i], 1, s[i + 1], 1)
        if s[i].lower() in i2:
            if 2 <= i and is_be_verb(s[i - 2]):
                store_word(store, s[i], 0, s[i - 1], 2)
            if i < len(s) - 1:
                store_word(store, s[i], 1, s[i + 1], 2)
"""----------------------------Comparing Freq------------------------------"""


def compare_freq(dict):
    lst = list(dict.keys())
    for i in range(len(lst)):
        syn1 = lst[i]
        cap1 = dict[syn1][0]  # capture of 1nd iter

        for j in range(i + 1, len(lst)):
            syn2 = lst[j]
            cap2 = dict[syn2][0]  # capture of 2nd iter
            if cap1.word == cap2.word:
                continue

            similarity = wn.wup_similarity(syn1, syn2)
            if syn1.pos() == syn2.pos() and similarity is not None and similarity > 0.5:
                if dict[syn1][1] > dict[syn2][1]:
                    print(make_phrase(cap1), "<<", cap2.word)
                else:
                    print(cap1.word, ">>", make_phrase(cap2))


def make_phrase(capture):
    if capture.position == 0:
        return capture.word + ' ' + capture.adverb
    else:
        return capture.adverb + ' ' + capture.word


compare_freq(store.adverb)
compare_freq(store.adjective)
compare_freq(store.verb)
result = Result()





