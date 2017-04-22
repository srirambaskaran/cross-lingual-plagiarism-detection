import codecs
import os
import re
import sys
import ConfigParser
import math
import numpy as np
import Queue as Q
import cPickle as pickle
from scipy import spatial
from collections import defaultdict
from sklearn.model_selection import train_test_split, cross_val_score, ShuffleSplit
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json

def sigmoid(x):
  return 1 / (1 + math.exp(-x))

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
k = int(configs["k"])
output_file = open(configs["output_file"],"w")

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

english = np.asarray(english)
foreign = np.asarray(foreign)

json_file = open('nn_sequence_embedding.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("nn_sequence_weights.txt")

loaded_model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
# scores = loaded_model.evaluate(english, foreign)
# print("\n%s: %.2f%%" % (loaded_model.metrics_names[1], scores[1]*100))

output = defaultdict()
actual = {}
correct = 0
total = 0
for i in range(len(english)):
	prediction = loaded_model.predict(english[i].reshape(1,-1))
	output[i] = Q.PriorityQueue()
	actual[i] = (None, 0.0) 
	for j in range(len(foreign)):
		fo_line =   [j]
		score = 1-spatial.distance.cosine(prediction[0], fo_line)
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
print float(correct)/ float(total)
output_file.close()