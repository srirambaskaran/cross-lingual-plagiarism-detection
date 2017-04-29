import sys
import word2vec_train
import precision
import ConfigParser


def read_config(file, section):
	Config = ConfigParser.ConfigParser()
	Config.read(file)
	configs = {}
	options = Config.options(section)
	for option in options:
		configs[option] = Config.get(section, option)
	return configs

def set_config(file, section, key, value):
	Config = ConfigParser.ConfigParser()
	Config.read(file)
	Config.set(section, key, value)
	Config.write(open(file,'w'))


num_times=int(sys.argv[3])
dimensions = [200]
section = sys.argv[2]
config_file=sys.argv[1]
all_average_precisions = {}
for dimension in dimensions:
	all_precisions = []
	set_config(config_file, section, 'dimension_input',dimension)
	for i in range(num_times): 
		print "Dimension: "+str(dimension)+" Iteration: "+str(i)
		output_file = word2vec_train.main(config_file, section)
		precisions = precision.main(output_file)
		all_precisions.append(precisions)
		print("+++++++++++++++++++++++++++++++\n")

	average_precision=[0,0,0,0]
	for precisions in all_precisions:
		average_precision[0]+=precisions[0]/num_times
		average_precision[1]+=precisions[1]/num_times
		average_precision[2]+=precisions[2]/num_times
		average_precision[3]+=precisions[3]/num_times

	all_average_precisions[dimension] = [average_precision[0], average_precision[1], average_precision[2], average_precision[3]]
	print "Accuracy: "+str(average_precision[0])+"\t"+str(average_precision[1])+"\t"+str(average_precision[2])+"\t"+str(average_precision[3])

for dimension in dimensions:
	print str(dimension)+"\t"+str(all_average_precisions[dimension][0])+"\t"+str(all_average_precisions[dimension][1])+"\t"+str(all_average_precisions[dimension][2])+"\t"+str(all_average_precisions[dimension][3])