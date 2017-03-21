import xml.etree.ElementTree
import codecs

root = xml.etree.ElementTree.parse('webcrawl-deen-sample.tmx').getroot()

tuTags = root.findall("body/tu")

f = codecs.open("parallel_10000_sample.txt", "w", "utf-8")
for tu in tuTags:
    print(tu.attrib["tuid"])
    tuvs = tu.findall("tuv")
    en_sentence = ""
    de_sentence = ""

    for tuv in tuvs:
        lang = tuv.attrib["lang"]
        if lang == "en":
            en_sentence = tuv[2].text
        else:
            de_sentence = tuv[2].text

    f.write(en_sentence+"\t"+de_sentence+"\n")

f.close()