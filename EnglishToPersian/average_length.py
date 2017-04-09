
import codecs
import numpy

file = codecs.open("../data/Hindi-English Parallel/hindi-parallel-tides-train.txt","r","utf-8")
total = 0
ratio = 0.0
ratios = []
for line in file:
	total+=1
	tokens = line.split("\t")
	english = len(tokens[1].split(" "))
	foreign = len(tokens[2].split(" "))
	ratios.append(float(foreign)/float(english))
	ratio+= float(foreign)/float(english)

print float(ratio)/total
print numpy.std(ratios)