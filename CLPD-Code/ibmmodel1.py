#! /usr/bin/env python
# coding:utf-8

import collections
import decimal
import nltk
import codecs
from operator import itemgetter
from decimal import Decimal as D
from nltk import word_tokenize
from pSCRDRtagger.RDRPOSTagger import RDRPOSTagger
from Utility.Utils import readDictionary

# set deciaml context
decimal.getcontext().prec = 4
decimal.getcontext().rounding = decimal.ROUND_HALF_UP

def _constant_factory(value):
    '''define a local function for uniform probability initialization'''
    #return itertools.repeat(value).next
    return lambda: value

def checktags(e_tag, f_tag):
  noun = (e_tag.startswith("NN") and  (f_tag.endswith("NOUN") or f_tag == "PRON"))
  verb = (e_tag.startswith("VB") and  f_tag.endswith("VERB"))

  return noun or verb


def _train(corpus, loop_count=1000):
    f_keys = set()
    for (es, fs) in corpus:
        for (f,tag) in fs:
            f_keys.add(f)
    # default value provided as uniform probability)
    t = collections.defaultdict(_constant_factory(D(1.0/len(f_keys))))

    # loop
    for i in range(loop_count):
        count = collections.defaultdict(D)
        total = collections.defaultdict(D)
        s_total = collections.defaultdict(D)
        for (es, fs) in corpus:
            # compute normalization
            for (e,e_tag) in es:
                s_total[e] = D()
                for (f,f_tag) in fs:
                    if checktags(e_tag, f_tag):
                        s_total[e] += t[(e, f)]
            for (e,e_tag) in es:
                for (f,f_tag) in fs:
                    if checktags(e_tag, f_tag):
                        count[(e, f)] += t[(e, f)] / s_total[e] if s_total[e] != 0 else 0
                        total[f] += t[(e, f)] / s_total[e] if s_total[e] != 0 else 0

        # estimate probability
        for (e, f) in count.keys():
            #if count[(e, f)] == 0:
            #    print(e, f, count[(e, f)])
            t[(e, f)] = count[(e, f)] / total[f] if total[f] != 0 else 0

    return t


def train(sentences, loop_count=1000):
    corpus = [(es.split(), fs.split()) for (es, fs) in sentences]
    return _train(corpus, loop_count)

def readlines(file, encode):
    lines = []
    with open(file, 'r') as f:
        for i,l in enumerate(f):
            lines.append(l.decode('UTF-8'))
    if encode:
      return [line.encode("UTF-8") for line in lines]
    else:
      return lines

if __name__ == '__main__':
    
    SENTENCES = []
    i = 0
    
    foreign_language = "Hindi"
    
    model_rdr = "./Models/UniPOS/UD_"+foreign_language+"/train.UniPOS.RDR"
    model_dict = "./Models/UniPOS/UD_"+foreign_language+"/train.UniPOS.DICT"

    foreign_language_tagger = RDRPOSTagger()
    foreign_language_tagger.constructSCRDRtreeFromRDRfile(model_rdr)
    foreign_language_dictionary = readDictionary(model_dict)

    # Reading Europarl dataset
    # english_lines = readlines("../data/news-commentary-v7.cs-en.en", False)
    # foreign_lines = readlines("../data/news-commentary-v7.cs-en.cs", True)
    # output_file = codecs.open("../data/news=commentry-cs-en.txt","w","utf-8")
    # for i in range(0,len(english_lines)):
    #     i += 1
    #     if i == 9000:
    #         break;
    #     english_words = nltk.pos_tag(word_tokenize(english_lines[i]))
    #     foreign_words = foreign_language_tagger.tagRawSentence(foreign_language_dictionary, foreign_lines[i])
    #     SENTENCES.append( (english_words, foreign_words) )

    # Reading custom created format
    file = codecs.open("../data/Hindi-English Parallel/hindi-parallel-tides-train.txt","r","utf-8")
    output_file = codecs.open("../data/Hindi-English Parallel/hindi-english-bilingual.txt","w","utf-8")
    i = 0
    for line in file:
        i += 1
        # if i == 100000:
        #     break;
        tokens = line.split("\t")
        english_words_tagged = nltk.pos_tag(word_tokenize(tokens[1]))
        foreign_words = foreign_language_tagger.tagRawSentence(foreign_language_dictionary, tokens[2].encode("UTF-8"))

        SENTENCES.append( (english_words_tagged, foreign_words) )

    print "READ INPUT"
    t = _train(SENTENCES, loop_count=10)
    for (e, f), val in t.items():
        output_file.write(e+"\t"+f.decode("utf-8")+"\t"+str(val)+"\n")
        print(e+"\t"+f.decode("utf-8")+"\t"+str(val))