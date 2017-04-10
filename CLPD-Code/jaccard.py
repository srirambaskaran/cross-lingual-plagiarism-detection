import codecs
import collections
import Queue as Q
from collections import defaultdict
import cPickle as pickle

def jaccard(set1, set2):
	intersection = set1.intersection(set2)
	union = set1.union(set2)
	return float(len(intersection))/float(len(union))

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


def readlines(file, encode):
	lines = []
	with open(file, 'r') as f:
		for i,l in enumerate(f):
			lines.append(l.decode('UTF-8'))
	if encode:
		return [line.encode("UTF-8") for line in lines]
	else:
		return lines

def read_pickle_dict(file):
	with open(file, 'rb') as f:
		dict = pickle.load(f)
		return dict

def get_max_prob_word(words):
	max_val = float("-inf")
	selected_word=""
	for word in words:
		if words[word] > max_val:
			max_val = words[word]
			selected_word = word
	return selected_word

if __name__ == "__main__":
	SENTENCES = []

	#Reading Europarl forat
	english_lines = readlines("../data/news-commentary-v7.cs-en.en", False)
	foreign_lines = readlines("../data/news-commentary-v7.cs-en.cs", True)

	# Dictionaries - custom made from ibm1 and standard off the shelf
	# bilingual_dictionary = read_dictionary("../data/Hindi-English Parallel/hindi-english-bilingual-copy.txt")	
	# bilingual_dictionary = read_pickle_dict("../data/en_hi.dict.pickle")


	# bilingual_dictionary = read_dictionary("../data/news-commentary-cs-en.txt")
	bilingual_dictionary = read_pickle_dict("../data/en_cs.dict.pickle")
	

	#Reading custom foramt
	# file = codecs.open("../data/Hindi-English Parallel/hindi-parallel-tides-test.txt","r","utf-8")
	# english_lines = []
	# foreign_lines = []
	# for line in file:
	# 	tokens = line.split("\t")
	# 	english_lines.append(tokens[1].strip())
	# 	foreign_lines.append(tokens[2].strip())


	# Common code for 2 fomats
	# output_file = codecs.open("../data/Hindi-English Parallel/hindi-parallel-tides-simple2-top10.txt","w","utf-8")
	output_file = codecs.open("../data/news-commentry-cs-en-simple-top10.txt","w","utf-8")

	k=10
	output = defaultdict()
	actual = {}
	correct = 0
	total = 0
	for i in range(0,len(english_lines)):
		english_sentence = english_lines[i]
		english_words = english_sentence.split(" ")
		
		output[i] = Q.PriorityQueue()
		actual[i] = (None, 0.0) 
		if i == 500:
			break
		translated_words = []
		for e in english_words:
			if e in bilingual_dictionary:

				# Two ways to get translated word.
				# translated_words.append(get_max_prob_word(bilingual_dictionary[e]))
				translated_words.append(bilingual_dictionary[e][0])
		
		for j in range(0, len(foreign_lines)):
			if j == 500:
				break
			foreign_sentence = foreign_lines[j]

			# Based on the file format of dictionary.
			# foreign_words = [word.encode("UTF-8") for word in foreign_sentence.split(" ")]
			foreign_words = foreign_sentence.split(" ")
			
			score = jaccard(set(translated_words), set(foreign_words))
			
			if i == j:
				actual[i] = (i,score)
			output[i].put( (-score, score, j))
		total+=1
		score_percent=0
		for c in range(0,k):
			(priority, val, foreign_id) = output[i].get()
			output_file.write(str(i)+"\t"+str(foreign_id)+","+str(val)+"\t"+str(actual[i])+"\n")
			if foreign_id == i:
				correct+=1

	output_file.close()
	print float(correct)/float(total)