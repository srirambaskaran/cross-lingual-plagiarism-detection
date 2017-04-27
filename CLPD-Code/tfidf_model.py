import codecs
import cPickle as pickle
import math
from collections import defaultdict

def tfidf(lines):
	length = len(lines)
	n_counts = {}
	tfidf_val = {}
	tf = {}
	for line in lines:
		seen_words = []
		words = line.strip().split()
		tf[line] = {}
		for word in words:
			if word in tf[line]:
				tf[line][word] +=1
			else:
				tf[line][word] = 1
			
			if word not in seen_words:
				seen_words.append(word)
				if word in n_counts:
					n_counts[word] += 1
				else:
					n_counts[word] = 1

	print "Computed TF and n-counts"
	for line in lines:
		words = line.strip().split()
		tfidf_val[line] = {}
		for word in words:
			tfidf_val[line][word] = tf[line][word]*math.log(float(length)/(n_counts[word]))

	print "Computed TF-IDF"
	return tfidf_val

file = codecs.open("../data/Hindi-English Parallel/hindi-parallel-tides-train.txt","r","utf-8")
english_lines = []
foreign_lines = []
n_count = defaultdict()
tfidf_val = defaultdict(dict)

for line in file:
	tokens = line.split("\t")
	english_lines.append(tokens[1].strip())
	foreign_lines.append(tokens[2].strip())

tfidf_val = tfidf(english_lines)
pickle.dump(tfidf_val, open("tfidf_en.pickle","wb"))

print "English over"
tfidf_val = tfidf(foreign_lines)

pickle.dump(tfidf_val, open("tfidf_hi.pickle","wb"))
print "Hindi over"