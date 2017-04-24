import sys
import cPickle as pickle
import numpy
import codecs

inp_file = open(sys.argv[1], 'rb')
out_file = sys.argv[2]
words, embeddings = pickle.load(inp_file)
words_dict = {}
output_file = codecs.open(out_file,"w","utf-8")

for i, word in enumerate(words):
	output_file.write(word)
	for j in range(len(embeddings[i])):
		output_file.write(","+str(embeddings[i][j]))
	output_file.write("\n")

inp_file.close()
output_file.close()