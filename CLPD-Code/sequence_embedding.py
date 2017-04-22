import codecs
import os
import re
import sys
import ConfigParser
import numpy as np
from scipy import spatial
import cPickle as pickle
import sklearn as sk
from sklearn import linear_model
from sklearn.model_selection import train_test_split, cross_val_score, ShuffleSplit
from sklearn.metrics import r2_score

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
	
	# if foreign_total == 0:
	# 	continue
	# if english_total == 0:
	# 	continue
	# english_average = np.divide(english_average, english_total)
	# foreign_average = np.divide(foreign_average, foreign_total)
	english.append(english_average)
	foreign.append(foreign_average)

print "Fitting a linear regression model"
regression = linear_model.LinearRegression()
# english_train, english_test, foreign_train, foreign_test = train_test_split(english, foreign, test_size=0.2, random_state=0)
# regression.fit(english_train, foreign_train)
# pickle.dump(regression,open("linear_mode.pickle","wb"))

scores = cross_val_score(regression, english, foreign, cv=ShuffleSplit(n_splits=10, test_size=0.1, random_state=0))
print scores

# print('Coefficients: \n'+str(regression.coef_))
# print regression.predict(english_test[0].reshape(1,-1))
# print foreign_test[0]
# v1 = [1,2,3]
# v2 = [5,2,4]
# print np.mean((v1 - v2) ** 2)
# print("Mean squared error: %.2f" % np.mean((regression.predict(english_test) - foreign_test) ** 2))
# print("R2 Score: %.2f" % r2_score(foreign_test,regression.predict(english_test)))
