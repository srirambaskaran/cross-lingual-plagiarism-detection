import xml.etree.ElementTree
import codecs

root = xml.etree.ElementTree.parse('../data/wikititles-2014_enfa.xml').getroot()

translations = root.findall("translation")

f = codecs.open("parallel_corpus_en_fa.txt", "w", "utf-8")
for translation in translations:
    translation_id = translation.attrib["id"]
    print(translation_id)
    entries = translation.findall("entry")
    en_sentence = ""
    fa_sentence = ""

    for entry in entries:
        lang = entry.attrib["lang"]
        if lang == "en":
            en_sentence = entry.text
        else:
            fa_sentence = entry.text

    f.write(translation_id+"\t"+en_sentence+"\t"+fa_sentence+"\n")

f.close()