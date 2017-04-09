import re
import codecs
import random


en_hi_file = codecs.open("./data/Hindi-English Parallel/hindencorp05.plaintext","r","utf-8")
train_file = codecs.open("./data/Hindi-English Parallel/hindi-parallel-tides-train.txt","w","utf-8")
test_file = codecs.open("./data/Hindi-English Parallel/hindi-parallel-tides-test.txt","w","utf-8")

lines = []
i = 0
percent_split = 0.99
for line in en_hi_file:
	tokens = line.split("\t")
	if tokens[0] == "tides":
		i+=1
		lines.append(tokens[3].strip()+"\t"+tokens[4].strip())

random.shuffle(lines)
train_size = i*percent_split
test_size = i-train_size
i = 0
for line in lines:
	i+=1
	if i <= train_size:
		train_file.write(str(i)+"\t"+line+"\n")
	else:
		test_file.write(str(i)+"\t"+line+"\n")

train_file.close()
test_file.close()