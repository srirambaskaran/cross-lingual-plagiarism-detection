
file = open("Hindi-English Parallel/hindi-parallel-tides-simple-top10.txt","r")

correct_1 = 0
correct_3 = 0
correct_5 = 0

total = 0

lines = file.readlines()
line_num = 0 
while True:
	if line_num >= len(lines):
		break
	total+=1
	for i in range(0,10):
		line = lines[line_num]
		tokens = line.split("\t")
		current = tokens[0] 
		selected = tokens[1].split(",")[0]
		if i < 1 and current == selected:
			correct_1+=1
		if i < 3 and current == selected:
			correct_3+=1
		if i < 5 and current == selected:
			correct_5+=1
		line_num+=1

print str(float(correct_1)/float(total))+"\t"+str(float(correct_3)/float(total))+"\t"+str(float(correct_5)/float(total))