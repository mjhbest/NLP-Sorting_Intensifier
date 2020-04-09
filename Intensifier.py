import nltk
from nltk.corpus import wordnet as wn

def recursive_add_adverb(adverb_list):
	print("now : ",adverb_list)
	plus1_adverb = adverb_list
	new_set = set(plus1_adverb)
	for pa in plus1_adverb:
		for w in wn.synsets(pa):
			if w.pos() == 'r' :
				print('word : {:15}'.format(str(pa)),'synset : {:20}'.format(str(w)), w.lemma_names(),w.examples())
				new_set.update(w.lemma_names())
	return list(new_set)


adverb = ['highly']
for i in range(5):
	adverb = recursive_add_adverb(adverb)
print(adverb)