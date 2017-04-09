import re, codecs

f = codecs.open("../data/English-Hindi Dict/noun.txt","r","utf-8")
outf = codecs.open("../data/english-hindi-dict.txt","a","utf-8")

for line in f:
	tokens = line.split(": ")
	all_words = tokens[1].strip().split(" ");
	for word in all_words:
		outf.write(tokens[0].replace("_"," ")+"\t"+word.replace("_"," ")+"\n")

outf.close()