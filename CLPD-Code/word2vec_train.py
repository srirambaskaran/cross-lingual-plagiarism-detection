import word2vec
import ConfigParser
import codecs
import numpy as np
from sklearn import linear_model
from sklearn.model_selection import train_test_split, cross_val_score, ShuffleSplit
import Queue as Q
from collections import defaultdict
from scipy import spatial
from sklearn.metrics import r2_score, mean_squared_error
import scipy.spatial as scpPT
# inFile = codecs.open('../DataCleaning/Bible/en_hi_bible_train.txt','r',encoding="utf-8")

# eng_sents =[]
# hindi_sents =[]

# for line in inFile:
#     token=line.strip().split('\t')
#     eng_sents.append(token[1])
#     hindi_sents.append((token[2]))
# inFile.close()

# eng_out_sents = codecs.open('../DataCleaning/Bible/eng_out_sents.txt','w',encoding="utf-8")
# for l1 in eng_sents:
#     eng_out_sents.write(l1+'\n')
# eng_out_sents.close()
# hindi_out_sents = codecs.open('../DataCleaning/Bible/hindi_out_sents.txt','w',encoding="utf-8")
# for l2 in hindi_sents:
#     hindi_out_sents.write(l2+'\n')
# hindi_out_sents.close()


# word2vec.word2vec('../DataCleaning/Bible/eng_out_sents.txt', '../DataCleaning/Bible/English_outs.bin', size=50, verbose=True)
# word2vec.word2vec('../DataCleaning/Bible/hindi_out_sents.txt', '../DataCleaning/Bible/Hindi_outs.bin', size=50, verbose=True)
english_embedding = word2vec.load('../DataCleaning/Bible/English_outs.bin')
foreign_embedding = word2vec.load('../DataCleaning/Bible/Hindi_outs.bin')



#v1 = English_model['best']
#v2 = English_model['water']

#print(1 - scpPT.distance.cosine(v1, v2))
#print (Hindi_model['go'])

def read_config(file, section):
    Config = ConfigParser.ConfigParser()
    Config.read(file)
    configs = {}
    options = Config.options(section)
    for option in options:
        configs[option] = Config.get(section, option)
    return configs



arg1= 'sequence_embedding.config'
arg2 = 'Sequence'

configs = read_config(arg1,arg2)

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
  e = tokens[0]
  f = tokens[1]
  p = float(tokens[2])

  if e in e_to_f:
   e_to_f[e][f] = p
  else:
   e_to_f[e] = {}
   e_to_f[e][f] = p

 return e_to_f

# bilingual_dictionary = read_dictionary('../DataCleaning/Bible/en_hi_bible_ibm1.txt')

dimension_input = 50
file = codecs.open('../DataCleaning/Bible/en_hi_bible_train.txt',"r","utf-8")
english_lines = []
foreign_lines = []
for line in file:
    #print (line)
    tokens = line.split("\t")
    #print ((tokens))
    english_lines.append(tokens[1].strip())
    foreign_lines.append(tokens[2].strip())

english = []
foreign = []
for i in range(0, len(foreign_lines)):
    foreign_words = foreign_lines[i].split()
    english_words = english_lines[i].split()

    english_average = np.full((dimension_input), 0.0)
    english_total = 0
    for word in english_words:
        if word in english_embedding:
            english_average += english_embedding[word]
            english_total += 1

    foreign_average = np.full((dimension_input), 0.0)
    foreign_total = 0
    for word in foreign_words:
        if word in foreign_embedding:
            foreign_average += foreign_embedding[word]
            foreign_total+=1

    # english_average = np.divide(english_average,english_total)
    # foreign_average = np.divide(foreign_average, foreign_total)
    if foreign_total == 0:
        print foreign_lines[i]
    if english_total == 0:
        print english_lines[i]
    english.append(english_average)
    foreign.append(foreign_average)

english = np.asarray(english)
foreign = np.asarray(foreign)
english_train, english_test, foreign_train, foreign_test = train_test_split(english, foreign, test_size=0.01, random_state=0)

print ("Fitting a linear regression model")
regression = linear_model.LinearRegression()

# scores = cross_val_score(regression, english, foreign, cv=ShuffleSplit(n_splits=10, test_size=0.1, random_state=0))
# print (scores)
regression.fit(english_train, foreign_train)
foreign_test_pred = regression.predict(english_test)
print("Mean squared error: %.2f" % np.mean((regression.predict(english_test) - foreign_test) ** 2))
print("R2 Score: %.2f" % r2_score(foreign_test,regression.predict(english_test)))

output = defaultdict()
actual = {}
correct = 0
total = 0
k=10
for i in range(len(english_test)):
    prediction = foreign_test_pred[i]
    output[i] = Q.PriorityQueue()
    actual[i] = (None, 0.0)
    for j in range(len(foreign_test)):
        fo_line =  foreign_test[j]
        score = mean_squared_error(fo_line, prediction)
        # score = 1-spatial.distance.cosine(fo_line, prediction)
        if i == j:
            actual[i] = (i,score)
        output[i].put( (score, score, j))
    total+=1
    score_percent=0
    for c in range(0,k):
        (priority, val, foreign_id) = output[i].get()
    # print(str(i)+"\t"+str(foreign_id)+","+str(val)+"\t"+str(actual[i]))
        if foreign_id == i:
            correct += 1

print (float(correct)/float(total))