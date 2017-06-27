import numpy as np
import pandas as pd
import nltk
import metaphone

def text_file_to_tokens(filepath):
    f = open(filepath, 'r')
    txt = f.read()
    f.close()
    return nltk.word_tokenize(txt)

def remove_stopwords(tokens, ponct=True, language="english"):
    stop = set(nltk.corpus.stopwords.words(language))
    if ponct:
        stop.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}'])
    l = []
    for token in tokens:
        if token.lower().strip() not in stop:
            l.append(token)
    return l

def extract_drug_names(l, names):
    names_low = [name.lower().strip() for name in names]
    names_meta = [metaphone.doublemetaphone(name) for name in names]
    result = []
    for x in l:
        x_low = x.lower().strip()
        if x_low in names_low:
            result.append((x, "true_eq"))
        elif metaphone.doublemetaphone(x_low) in names_meta:
            result.append((x, "meta_eq"))

    return result

if __name__=="__main__":
    input_file = "file_modified.txt"
    tokens = text_file_to_tokens(input_file)
    clean_tokens = remove_stopwords(tokens)
    # TODO: drugs = rxnormhandler.list_drug_names()
    drugs = ['methadone', 'protonix', 'lovenox', 'azithromycin']

    drug_names = extract_drug_names(clean_tokens, drugs)
    print(drug_names)
