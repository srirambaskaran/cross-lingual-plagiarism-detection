import codecs
import os
import re
import sys
import ConfigParser
import numpy as np
from scipy import spatial
import cPickle as pickle

def read_config(file, section):
	Config = ConfigParser.ConfigParser()
	Config.read(file)
	configs = {}
	options = Config.options(section)
	for option in options:
		configs[option] = Config.get(section, option)
	return configs


configs = read_config(sys.argv[1],sys.argv[2])
file = codecs.open(configs["input_file"],"r","utf-8")
english_lines = []
foreign_lines = []
for line in file:
	tokens = line.split("\t")
	english_lines.append(tokens[1].strip())
	foreign_lines.append(tokens[2].strip())

english_embedding = pickle.load(open(configs['english_embeddings'],"rb"))
foreign_embedding = pickle.load(open(configs['foreign_embeddings'],"rb"))
similarity = 0.0
similarities = []
np.seterr(all='raise')
total = 0
for i in range(0, len(foreign_lines)):
	foreign_words = foreign_lines[i].split(" ")
	english_words = english_lines[i].split(" ")

	english_average = np.full((64), 0.0)
	english_total = 0
	for word in english_words:
		if word in english_embedding:
			english_average += english_embedding[word]
			english_total+=1

	foreign_average = np.full((64), 0.0)
	foreign_total = 0
	for word in foreign_words:
		if word in foreign_embedding:
			foreign_average += foreign_embedding[word]
			foreign_total+=1
	
	if foreign_total == 0:
		continue
	if english_total == 0:
		continue
	english_average = np.divide(english_average, english_total)
	foreign_average = np.divide(foreign_average, foreign_total)

	
	if foreign_total !=0 and english_total != 0:
		total+=1
		similarity = np.dot(english_average, foreign_average) / (np.linalg.norm(english_average) * np.linalg.norm(foreign_average))
		similarities.append(similarity)

print "Maximum Similarity: " + str(max(similarities))
print "Minimum Similarity: " + str(min(similarities))
print "Average Similarity: " + str(sum(similarities)/len(similarities))

