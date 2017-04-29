import sys
import ConfigParser

def main(argv1):
	file = open(argv1)

	correct_1 = 0
	correct_3 = 0
	correct_5 = 0
	correct_10 = 0

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
			val = float(tokens[1].split(",")[1])
			if i < 1 and current == selected and val != 0:
				correct_1+=1
			if i < 3 and current == selected and val != 0:
				correct_3+=1
			if i < 5 and current == selected and val != 0:
				correct_5+=1
			if i < 10 and current == selected and val != 0:
				correct_10+=1
			line_num+=1

	print "Top-1=> Correct: "+ str(correct_1)+ " Accuracy:"+str(float(correct_1)/float(total))
	print "Top-3=> Correct: "+ str(correct_3)+ " Accuracy:"+str(float(correct_3)/float(total))
	print "Top-5=> Correct: "+ str(correct_5)+ " Accuracy:"+str(float(correct_5)/float(total))
	print "Top-10=> Correct: "+ str(correct_10)+ " Accuracy:"+str(float(correct_10)/float(total))

	print str(float(correct_1)/float(total))+"\t"+str(float(correct_3)/float(total))+"\t"+str(float(correct_5)/float(total))+"\t"+str(float(correct_10)/float(total))
	return [float(correct_1)/float(total), float(correct_3)/float(total), float(correct_5)/float(total), float(correct_10)/float(total)]
if __name__ == '__main__':
	main(sys.argv[1])