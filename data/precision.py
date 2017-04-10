import sys
import ConfigParser

def read_config(file, section):
	Config = ConfigParser.ConfigParser()
	Config.read(file)
	configs = {}
	options = Config.options(section)
	for option in options:
		configs[option] = Config.get(section, option)
	return configs

configs = read_config(sys.argv[1], sys.argv[2])
file = open(configs["output_file"])

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