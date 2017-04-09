import collections
import decimal
import nltk
import math
import codecs
from operator import itemgetter
from nltk import word_tokenize
from pSCRDRtagger.RDRPOSTagger import RDRPOSTagger
from Utility.Utils import readDictionary
from decimal import Decimal as D


foreign_language = "Hindi"
model_rdr = "./Models/UniPOS/UD_"+foreign_language+"/train.UniPOS.RDR"
model_dict = "./Models/UniPOS/UD_"+foreign_language+"/train.UniPOS.DICT"
foreign_language_tagger = RDRPOSTagger()
foreign_language_tagger.constructSCRDRtreeFromRDRfile(model_rdr)
foreign_language_dictionary = readDictionary(model_dict)
k = 10
mu = 1.10768678111 #for Hindi
sigma = 0.259916622673 #for Hindi

def pos_tag_english(english_sentence):
	english_words = nltk.pos_tag(word_tokenize(english_sentence))
	return english_words

def pos_tag_foreign(foreign_sentence):
	foreign_words = foreign_language_tagger.tagRawSentence(foreign_language_dictionary, foreign_sentence)
	return foreign_words


def readlines(file, encode):
	lines = []
	with open(file, 'r') as f:
		for i,l in enumerate(f):
			lines.append(l.decode('UTF-8'))
	if encode:
		return [line.encode("UTF-8") for line in lines]
	else:
		return lines
  
def read_dictionary(file):
	file = codecs.open(file,"r","utf-8")
	e_to_f = {}
	for line in file:
		tokens = line.split("\t")
		e = tokens[0];
		f = tokens[1];
		p = float(tokens[2]);

		if e in e_to_f:
			e_to_f[e][f] = p
		else:
			e_to_f[e] = {}
			e_to_f[e][f] = p

	return e_to_f

if __name__ == "__main__":
	SENTENCES = []
	# english_lines = readlines("../data/news-commentary-v7.cs-en.en", False)
	# foreign_lines = readlines("../data/news-commentary-v7.cs-en.cs", True)
	bilingual_dictionary = read_dictionary("../data/Hindi-English Parallel/hindi-english-bilingual-copy.txt")
	output_file = codecs.open("../data/Hindi-English Parallel/hindi-parallel-tides-matched.txt","w","utf-8")


	file = codecs.open("../data/Hindi-English Parallel/hindi-parallel-tides-test.txt","r","utf-8")
    # output_file = codecs.open("../data/Hindi-English Parallel/hindi-english-bilingual.txt","w","utf-8")

	english_lines = []
	foreign_lines = []
	for line in file:
		tokens = line.split("\t")
		english_lines.append(tokens[1].strip())
		foreign_lines.append(tokens[2].strip())

	output = {}
	actual = {}
	correct = 0
	total = 0
	for i in range(0,len(english_lines)):
		english_sentence = english_lines[i]
		english_words = pos_tag_english(english_sentence)
		len_english = float(len(english_words))
		if len_english == 0:
			continue
		output[i] = (None, float("-inf"))
		actual[i] = (None, float("-inf")) 
		if i == 500:
			break
		for j in range(0, len(foreign_lines)):
			if j == 500:
				break
			foreign_sentence = foreign_lines[j]
			foreign_words = foreign_sentence.split(" ")
			len_foreign = float(len(foreign_words))

			length_model = math.exp(-0.5 * (((len_foreign / len_english) - mu) / sigma)**2)
			
			transition_model = 0.0;
			for e,e_tag in english_words:
				if e in bilingual_dictionary:
					for f in foreign_words:
						if f in bilingual_dictionary[e]:
							transition_model += bilingual_dictionary[e][f]
						else:
							transition_model -= 0.001
			current, max_val = output[i];
			val = transition_model * length_model
			if i == j:
				actual[i] = (i,val)
			if max_val < val:
				output[i] = (j, val)
		if output[i][0] == actual[i][0]:
			correct+=1
		total+=1
		score_percent = (actual[i][1]-output[i][1])/(actual[i][1])
		output_file.write(str(i)+"\t"+str(output[i])+"\t"+str(actual[i])+"\t"+str(score_percent) + "\n")

	print float(correct)/float(total)
	output_file.close()