
file = open("news-commentry-cs-en-matched.txt","r")

correct = 0
total = 0
for line in file:
	tokens = line.split("\t")
	total+=1
	if tokens[0] == tokens[1].split(",")[0][1:]:
		correct+=1

print float(correct)/float(total)