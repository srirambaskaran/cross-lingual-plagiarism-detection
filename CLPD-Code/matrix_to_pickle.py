import sys
import cPickle as pickle
import numpy

inp_file = open(sys.argv[1], 'rb')
out_file = open(sys.argv[2], 'wb')
words, embeddings = pickle.load(inp_file)
words_dict = {}
for i, word in enumerate(words):
	words_dict[word] = embeddings[i,:]

pickle.dump(words_dict,out_file)
inp_file.close()
out_file.close()