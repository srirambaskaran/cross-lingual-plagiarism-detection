from __future__ import division, unicode_literals
import word2vec
import codecs
import os
import re
import sys
import math
import ConfigParser
import numpy as np
import cPickle as pickle
from collections import defaultdict
from sklearn.model_selection import train_test_split, cross_val_score, ShuffleSplit
from keras.models import Sequential
from keras.layers import Dense, Dropout

def read_config(file, section):
	Config = ConfigParser.ConfigParser()
	Config.read(file)
	configs = {}
	options = Config.options(section)
	for option in options:
		configs[option] = Config.get(section, option)
	return configs


configs = read_config(sys.argv[1],sys.argv[2])
file = codecs.open('../DataCleaning/Bible/en_hi_bible_train.txt',"r","utf-8")
dim = 50
english_lines = []
foreign_lines = []
for line in file:
	tokens = line.split("\t")
	english_lines.append(tokens[1].strip())
	foreign_lines.append(tokens[2].strip())


english_embedding = word2vec.load('../DataCleaning/Bible/English_outs.bin')
foreign_embedding = word2vec.load('../DataCleaning/Bible/Hindi_outs.bin')
# e_tfidf = pickle.load(open(configs['english_tfidf'],"rb"))
# f_tfidf = pickle.load(open(configs['foreign_tfidf'],"rb"))

english = []
foreign = []
for i in range(0, len(foreign_lines)):
	foreign_words = foreign_lines[i].split()
	english_words = english_lines[i].split()

	english_average = np.full((dim), 0.0)
	english_total = 0
	for word in english_words:
		if word in english_embedding:
			# english_average += e_tfidf[english_lines[i]][word]*english_embedding[word]
			english_average += english_embedding[word]
			english_total+=1

	foreign_average = np.full((dim), 0.0)
	foreign_total = 0
	for word in foreign_words:
		if word in foreign_embedding:
			# foreign_average += f_tfidf[foreign_lines[i]][word]*foreign_embedding[word]
			foreign_average += foreign_embedding[word]
			foreign_total+=1
	english.append(english_average)
	foreign.append(foreign_average)

english_train, english_test, foreign_train, foreign_test = train_test_split(english, foreign, test_size=0.01, random_state=0)
english_train = np.asarray(english_train)
english_test = np.asarray(english_test)
foreign_train = np.asarray(foreign_train)
foreign_test = np.asarray(foreign_test)

model = Sequential()
model.add(Dense(100, input_dim = 50, activation='relu'))
model.add(Dense(500, activation='relu'))
model.add(Dense(500, activation='relu'))
model.add(Dense(300, activation='relu'))
model.add(Dense(50, activation='linear'))
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

model.fit(english_train, foreign_train, epochs=100, batch_size=100)
scores = model.evaluate(english_test, foreign_test, verbose=2)
model_json = model.to_json()
with open("../DataCleaning/Bible/nn_bible_model.json", "w") as json_file:
	json_file.write(model_json)
model.save_weights("../DataCleaning/Bible/nn_bible_weights.txt")

print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))


