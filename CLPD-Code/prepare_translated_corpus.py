import nltk
import pandas
import codecs
from PyDictionary import PyDictionary
from hazm import word_tokenize as persian_word_tokenize
import re
from nltk import word_tokenize
from nltk.corpus import stopwords

def jaccard(set1, set2):
	intersection = set1.intersection(set2)
	union = set1.union(set2)
	return float(len(intersection))/float(len(union))

stop = set(stopwords.words('english'))
file = codecs.open("../data/parallel_corpus_en_fa.txt","r","utf-8")
output_file = codecs.open("../data/parallel_corpus_en_fa_translated.txt","w","utf-8")
word_dict = {}
dictionary_file = codecs.open("../data/wordsDict.txt","r","utf-8")
number_pattern = re.compile("^\d+$");

for word in dictionary_file:
	tokens = word.split("\t")
	word_dict[tokens[0]] = tokens[1].strip()
	# if tokens[0] in word_dict:
	# 	word_dict[tokens[0]].append(tokens[1].strip())
	# else:
	# 	word_dict[tokens[0]] = []
	# 	word_dict[tokens[0]].append(tokens[1].strip())

dictionary = PyDictionary()
i = 0
for line in file:
	i+=1
	tokens = line.split("\t")
	words = word_tokenize(tokens[1]);
	new_words = [token for token in tokens[1].lower().split() if token not in stop]
	out_of_vocab = False
	english_translated_words = set()
	persian_words = persian_word_tokenize(tokens[2])
	for word in new_words:
		number_match = number_pattern.match(word)
		if number_match:
			characters = list(word)
			fa_word = ""
			for character in characters:
				fa_word+=word_dict[character]
			english_translated_words.add(fa_word)
		else:
			if word in word_dict:
				english_translated_words.add(word_dict[word])
			# fa_word = dictionary.translate(word,"fa")
			# if fa_word != None:
			# 	english_translated_words.add(fa_word)
	jaccard_score = jaccard(english_translated_words, set(persian_words))
	output_file.write(tokens[0].strip()+"\t"+tokens[1].strip()+"\t"+tokens[2].strip()+"\t"+str(jaccard_score)+"\n")
	

output_file.close()


