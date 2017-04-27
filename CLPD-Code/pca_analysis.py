import codecs
import os
import re
import sys
import ConfigParser
import math
import numpy as np
import Queue as Q
import cPickle as pickle
from collections import defaultdict
from sklearn.model_selection import train_test_split, cross_val_score, ShuffleSplit
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import plotly.plotly as py

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

english = np.asarray(english)
foreign = np.asarray(foreign)

pca_english = PCA(n_components=10)
pca_english.fit(english)
pca_foreign = PCA(n_components=10)
pca_foreign.fit(foreign)
transform_english = pca_english.transform(english)
transform_foreign = pca_foreign.transform(foreign)

for i in range(len(transform_english)):
	if i == 100:
		break
	print str(len(transform_english[i]))+"\t"+str(transform_english[i][0])+"\t"+str(transform_english[i][1])

for i in range(len(transform_foreign)):
	if i == 100:
		break
	print str(len(transform_english[i]))+"\t"+str(transform_foreign[i][0])+"\t"+str(transform_foreign[i][1])