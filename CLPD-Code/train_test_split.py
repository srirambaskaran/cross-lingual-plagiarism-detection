from sklearn.model_selection import train_test_split
import codecs
import random

lines = []

combined = codecs.open("../DataCleaning/en_hi_bible.txt","r","utf-8")
for line in combined:
	lines.append(line)


random.shuffle(lines)

train_file = codecs.open("../DataCleaning/en_hi_bible_train.txt","w","utf-8")
test_file = codecs.open("../DataCleaning/en_hi_bible_test.txt","w","utf-8")
train_count = len(lines)/100*99
print train_count
j = 0
for i in range(len(lines)):
	train_file.write(lines[i])
	j+=1
	if j == train_count:
		break
	
train_file.close()

for k in range(j,len(lines)):
	test_file.write(lines[k])

test_file.close()