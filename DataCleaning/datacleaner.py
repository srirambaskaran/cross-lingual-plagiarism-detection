import xml.etree.ElementTree
import codecs

root = xml.etree.ElementTree.parse('../../../data/Bible/English.xml').getroot()

chapters = root.findall("text/body/div/div")

f = codecs.open("english_bible.txt", "w", "utf-8")
i = 1
for chapter in chapters:
    
    segments = chapter.findall("seg")

    for segment in segments:
        print i
        sentence = segment.text
        segment_id = segment.attrib["id"]
        if sentence is not None:
            f.write(segment_id.strip()+"\t"+sentence.strip()+"\n")

        i+=1
f.close()