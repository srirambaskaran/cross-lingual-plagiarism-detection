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

english = []
foreign = []
for i in range(0, len(foreign_lines)):
	foreign_words = foreign_lines[i].split()
	english_words = english_lines[i].split()

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
	english.append(english_average)
	foreign.append(foreign_average)


english_train, english_test, foreign_train, foreign_test = train_test_split(english, foreign, test_size=0.2, random_state=0)
english_train = np.asarray(english_train)
english_test = np.asarray(english_test)
foreign_train = np.asarray(foreign_train)
foreign_test = np.asarray(foreign_test)
print type(english_train)
print type(foreign_train)


model = Sequential()
model.add(Dense(100, input_dim = 64, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(64, activation='linear'))
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

model.fit(english_train, foreign_train, epochs=30, batch_size=100)
print model.predict(english_test[0].reshape(1,-1))
print foreign_test[0]
scores = model.evaluate(english_train, foreign_train)
model_json = model.to_json()
with open("nn_sequence_embedding.json", "w") as json_file:
	json_file.write(model_json)
model.save_weights("nn_sequence_weights.txt")

print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

