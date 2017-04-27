import codecs
import os
import re
import sys
import ConfigParser
import numpy as np
from collections import defaultdict
from scipy import spatial
import cPickle as pickle
import sklearn as sk
import Queue as Q
from sklearn import linear_model, svm
from sklearn.model_selection import train_test_split, cross_val_score, ShuffleSplit
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.decomposition import PCA

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

english = np.asarray(english)
foreign = np.asarray(foreign)
# pca_english = PCA(n_components=2)
# pca_english.fit(english)
# pca_foreign = PCA(n_components=2)
# pca_foreign.fit(foreign)
# transform_english = pca_english.transform(english)
# transform_foreign = pca_foreign.transform(foreign)

english_train, english_test, foreign_train, foreign_test = train_test_split(english, foreign, test_size=0.01, random_state=0)
# print "Fitting a linear regression model"
# regression = linear_model.Ridge(alpha = 0.01)
# regression.fit(english_train, foreign_train)

# foreign_test_pred = regression.predict(english_test)
# print("R2 Score: %.2f" % r2_score(foreign_test,foreign_test_pred))
output = defaultdict()
actual = {}
correct = 0
total = 0
k=10
for i in range(len(english_test)):
	prediction = english_test[i]
	output[i] = Q.PriorityQueue()
	actual[i] = (None, 0.0) 
	for j in range(len(foreign_test)):
		fo_line =  foreign_test[j]
		# score = mean_squared_error(fo_line, prediction)
		score = 1-spatial.distance.cosine(fo_line, prediction)
		if i == j:
			actual[i] = (i,score)
		output[i].put( (-score, score, j))
	total+=1
	score_percent=0
	for c in range(0,k):
		(priority, val, foreign_id) = output[i].get()
		# print(str(i)+"\t"+str(foreign_id)+","+str(val)+"\t"+str(actual[i]))
		if foreign_id == i:
			correct+=1
print float(correct)/ float(total)
# scores = cross_val_score(regression, english, foreign, cv=ShuffleSplit(n_splits=10, test_size=0.1, random_state=0))
# regression = svm.SVR()
# for degree in [3,4,5]:
# 	print "degree "+str(degree)
# 	model = make_pipeline(PolynomialFeatures(degree), linear_model.LinearRegression())
# 	model.fit(english_train, foreign_train)
# 	# regression = linear_model.Lasso()

# 	# regression.fit(english_train, foreign_train)
# 	# pickle.dump(regression,open("linear_mode.pickle","wb"))

# 	# scores = cross_val_score(regression, english, foreign, cv=ShuffleSplit(n_splits=10, test_size=0.1, random_state=0))
# 	# print scores

# 	# print('Coefficients: \n'+str(regression.coef_))
# 	# print regression.predict(english_test[0].reshape(1,-1))
# 	# print foreign_test[0]
# 	# v1 = [1,2,3]
# 	# v2 = [5,2,4]
# 	# print np.mean((v1 - v2) ** 2)
# 	print("Mean squared error: %.2f" % np.mean((model.predict(english_test) - foreign_test) ** 2))
# 	print("R2 Score: %.2f" % r2_score(foreign_test,model.predict(english_test)))