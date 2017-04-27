import codecs

e_file = codecs.open("english_bible.txt","r","utf-8")
h_file = codecs.open("hindi_bible.txt","r","utf-8")
combined = codecs.open("en_hi_bible.txt","w","utf-8")
english = {}
for line in e_file:
	tokens = line.strip().split("\t")
	segment_id = tokens[0]
	sentence = tokens[1]
	english[segment_id] = sentence


for line in h_file:
	tokens = line.strip().split("\t")
	segment_id = tokens[0]
	sentence = tokens[1]
	if segment_id in english:
		combined.write(segment_id + "\t" + english[segment_id]+ "\t" + sentence +"\n")

combined.close()
