# Cross Lingual Plagiarism Detection
## NLP Project

### Jaccard
.Standard
change '''mode''' to standard. Rename relevant output files.
.Alignment
change '''mode''' to standard. Rename relevant output files.

#### Bible corpus
```python jaccard.py jaccard.config Bible```

#### Newspaper Corpus
```python jaccard.py jaccard.config Newspaper```


### CLPD-ASA

#### Bible corpus
```python clpd_asa.py clpd_asa.config Bible```

#### Newspaper Corpus
```python clpd_asa.py clpd_asa.config Newspaper```



### VectorSim

## Bible corpus
```python word2vec_train.py.py word2vec_train.py.config Bible```

#### Newspaper Corpus
```python word2vec_train.py.py word2vec_train.py.config Newspaper```


use  ```word2vec_multiple_iter.py``` for iteratively running for various vector dimension values.
