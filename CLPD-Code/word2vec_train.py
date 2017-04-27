import word2vec
import ConfigParser
import codecs
import sys
import math
import numpy as np
import Queue as Q
from scipy import spatial
from sklearn import linear_model
from collections import defaultdict
from sklearn.metrics import r2_score, mean_squared_error

#Reading configuration
def read_config(file, section):
    Config = ConfigParser.ConfigParser()
    Config.read(file)
    configs = {}
    options = Config.options(section)
    for option in options:
        configs[option] = Config.get(section, option)
    return configs

#Reading paralle corpus
def read_parallel_corpus(file_lines, dimension_input):
    english_lines = []
    foreign_lines = []
    for line in file_lines:
        tokens = line.split("\t")
        english_lines.append(tokens[1].strip())
        foreign_lines.append(tokens[2].strip())

    english = []
    foreign = []
    for i in range(0, len(foreign_lines)):
        foreign_words = foreign_lines[i].split()
        english_words = english_lines[i].split()
        english_final = np.full((dimension_input), 0.0)
        english_total = 0
        for word in english_words:
            if word in english_embedding:
                english_final += english_embedding[word]
                english_total += 1
        foreign_final = np.full((dimension_input), 0.0)
        foreign_total = 0
        for word in foreign_words:
            if word in foreign_embedding:
                foreign_final += foreign_embedding[word]
                foreign_total+=1
        english.append(english_final)
        foreign.append(foreign_final)
    return np.asarray(english), np.asarray(foreign)


configs = read_config(sys.argv[1],sys.argv[2])
train_file_obj = codecs.open(configs['train_file'],'r','utf-8')
train_lines = train_file_obj.readlines()
train_file_obj.close()
train_word_vectors = configs['train_word_vectors'].lower()
dimension_input = int(configs['dimension_input'])

# Training word2vec for the training data
if train_word_vectors == 'true':
    english_sents =[]
    foreign_sents =[]
    for line in train_lines:
        token=line.strip().split('\t')
        english_sents.append(token[1])
        foreign_sents.append((token[2]))

    eng_out_sents = codecs.open(configs['english_temp'],'w',encoding="utf-8")
    for l1 in english_sents:
        eng_out_sents.write(l1+'\n')
    eng_out_sents.close()
    foreign_out_sents = codecs.open(configs['foreign_temp'],'w',encoding="utf-8")
    for l2 in foreign_sents:
        foreign_out_sents.write(l2+'\n')
    foreign_out_sents.close()

    word2vec.word2vec(configs['english_temp'], configs['english_embeddings'], size=dimension_input, verbose=True)
    word2vec.word2vec(configs['foreign_temp'], configs['foreign_embeddings'], size=dimension_input , verbose=True)


english_embedding = word2vec.load(configs['english_embeddings'])
foreign_embedding = word2vec.load(configs['foreign_embeddings'])

test_lines = codecs.open(configs['test_file'],'r','utf-8').readlines()

k=int(configs['k'])
mu = float(configs['mu'])
sigma = float(configs['sigma'])

english_train, foreign_train = read_parallel_corpus(train_lines, dimension_input)
english_test, foreign_test = read_parallel_corpus(test_lines, dimension_input)

print ("Fitting a linear regression model")
regression = linear_model.LinearRegression()
regression.fit(english_train, foreign_train)
print ("Completed Linear Regression!")

print ("Testing Linear Regression Model!")
foreign_test_pred = regression.predict(english_test)
print("R2 Score: %.2f" % r2_score(foreign_test,foreign_test_pred))

length_based_metric = configs['length_based_metric'].lower()
metric = configs['metric'].lower()
output = defaultdict()
actual = {}
correct = 0
total = 0
output_file = codecs.open(configs['output_ranking'],'w','utf-8')
for i in range(len(english_test)):
    prediction = foreign_test_pred[i]
    output[i] = Q.PriorityQueue()
    actual[i] = (None, 0.0)
    len_english = len(english_test)
    for j in range(len(foreign_test)):
        fo_line =  foreign_test[j]
        len_foreign = len(fo_line)
        score = 0
        if metric == 'cosine':
            score = spatial.distance.cosine(fo_line, prediction)
        elif metric == 'mean_squared_error':
            score = mean_squared_error(fo_line, prediction)
        if length_based_metric == 'true':
            length_model = math.exp(-0.5 * (((float(len_foreign) / len_english) - mu) / sigma)**2)
            score = length_model*score

        if i == j:
            actual[i] = (i,score)
        output[i].put( (score, score, j))
    total+=1
    score_percent=0
    for c in range(0,k):
        (priority, val, foreign_id) = output[i].get()
        output_file.write(str(i)+"\t"+str(foreign_id)+","+str(val)+"\t"+str(actual[i])+"\n")
        if foreign_id == i:
            correct += 1

output_file.close()
print ("Completed Testing!")