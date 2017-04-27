import sys
import collections
import decimal
import nltk
import math
import codecs
import Queue as Q
import ConfigParser
from operator import itemgetter
from collections import defaultdict
from nltk import word_tokenize
from pSCRDRtagger.RDRPOSTagger import RDRPOSTagger
from Utility.Utils import readDictionary
from decimal import Decimal as D

def read_config(file, section):
	Config = ConfigParser.ConfigParser()
	Config.read(file)
	configs = {}
	options = Config.options(section)
	for option in options:
		configs[option] = Config.get(section, option)
	return configs

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

configs = read_config(sys.argv[1], sys.argv[2])
foreign_language = configs["foreign_language"]
model_rdr = "./Models/UniPOS/UD_"+foreign_language+"/train.UniPOS.RDR"
model_dict = "./Models/UniPOS/UD_"+foreign_language+"/train.UniPOS.DICT"
foreign_language_tagger = RDRPOSTagger()
foreign_language_tagger.constructSCRDRtreeFromRDRfile(model_rdr)
foreign_language_dictionary = readDictionary(model_dict)
k = int(configs["k"])
mu = float(configs["mu"])
sigma = float(configs["sigma"])

file = codecs.open(configs["input_file"],"r","utf-8")
bilingual_dictionary = read_dictionary(configs["bilingual_dictionary"])
output_file = codecs.open(configs["output_file"],"w","utf-8")

english_lines = []
foreign_lines = []
for line in file:
	tokens = line.split("\t")
	english_lines.append(tokens[1].strip())
	foreign_lines.append(tokens[2].strip())
output = defaultdict()
actual = {}
correct = 0
total = 0
for i in range(0,len(english_lines)):
	english_sentence = english_lines[i]
	english_words = pos_tag_english(english_sentence)
	len_english = float(len(english_words))
	if len_english == 0:
		continue
	output[i] = Q.PriorityQueue()
	actual[i] = (None, float("-inf")) 
	for j in range(0, len(foreign_lines)):
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
		val = transition_model * length_model
		if i == j:
			actual[i] = (i,val)
		output[i].put((-val, val , j))
	total += 1
	
	for c in range(0,k):
		(priority, val, foreign_id) = output[i].get()
		output_file.write(str(i)+"\t"+str(foreign_id)+","+str(val)+"\t"+str(actual[i])+"\n")
		if foreign_id == i:
			correct += 1

output_file.close()