import codecs
import os
import re
import sys
import ConfigParser
import numpy as np
import cPickle as pickle
from collections import defaultdict
from sklearn.model_selection import train_test_split, cross_val_score, ShuffleSplit
from keras.models import Sequential
from keras.layers import Dense, Dropout

def get_max_prob_word(words):
	max_val = float("-inf")
	selected_word=""
	for word in words:
		if words[word] > max_val:
			max_val = words[word]
			selected_word = word
	return selected_word


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


def read_config(file, section):
	Config = ConfigParser.ConfigParser()
	Config.read(file)
	configs = {}
	options = Config.options(section)
	for option in options:
		configs[option] = Config.get(section, option)
	return configs


def read_pickle_dict(file):
	with open(file, 'rb') as f:
		dict = pickle.load(f)
		return dict

configs = read_config(sys.argv[1],sys.argv[2])
bilingual_dictionary = read_dictionary(configs["dictionary_file"])	
# bilingual_dictionary = read_pickle_dict(configs["dictionary_file"])

english_embedding = pickle.load(open(configs['english_embeddings'],"rb"))
foreign_embedding = pickle.load(open(configs['foreign_embeddings'],"rb"))
x = []
y = []
eng = 0
for word in bilingual_dictionary:
	if word in english_embedding:
		hindi_word = get_max_prob_word(bilingual_dictionary[word])
		# for hindi_word  in bilingual_dictionary[word]:
		if hindi_word in foreign_embedding:
			x.append(english_embedding[word])
			y.append(foreign_embedding[hindi_word])

print "Length: "+str(len(x))
english = np.asarray(x)
foreign = np.asarray(y)

model = Sequential()
model.add(Dense(100, input_dim = 64, activation='sigmoid'))
model.add(Dense(500, activation='sigmoid'))
model.add(Dense(100, activation='sigmoid'))
model.add(Dense(64, activation='linear'))
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

model.fit(english, foreign, epochs=30, batch_size=1)
scores = model.evaluate(english, foreign)
model_json = model.to_json()
with open("nn_word_embedding.json", "w") as json_file:
	json_file.write(model_json)
model.save_weights("nn_word_weights.txt")

print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

