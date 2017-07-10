import pandas as pd
import metaphone
import tqdm
import numpy as np


def load_rxnorm(paths):
    """
    Generate list of drug names based on rxnorm database.

    :param paths: dict | Dictionnary of path with table names as keys
    :return: pd.DataFrame | Data
    """
    df_rxnconso = pd.read_csv(paths['rxnconso'])
    df_rxnconso = df_rxnconso[df_rxnconso['SAB'] == "RXNORM"]

    return df_rxnconso


def add_metaphone_to_rxnorm(df_rxnconso):
    names = df_rxnconso['STR']
    names_low = [name.lower().strip() for name in names]
    names_meta = [metaphone.doublemetaphone(name) for name in names_low]
    df_rxnconso['low'] = names_low
    df_rxnconso['dmeta'] = names_meta
    print(df_rxnconso.values.shape)
    return df_rxnconso


def strict_equal_criteria(word1, word2):
    return word1 == word2


def levenshtein_distance(word1, word2):
    size1, size2 = len(word1), len(word2)
    dist = np.zeros((size1, size2))
    dist[:, 0] = np.range(size1)
    dist[0, :] = np.range(size2)

    for i in range(1, size1):
        for j in range(1, size2):
            cout = 1 - word1[i] == word2[j]
            dist[i, j] = min(dist[i-1, j] + 1, dist[i, j-1]+1, dist[i-1, j-1] + cout)

    return dist[size1-1, size2-1]


def levenshtein_criteria(distance):
    return distance < 4


def metaphone_criteria(word1, word2):
    word1_meta = metaphone.doublemetaphone(word1)
    word2_meta = metaphone.doublemetaphone(word2)
    metaphone_apply = word1_meta == word2_meta
    if metaphone_apply:
        levenshtein_dist = levenshtein_distance(word1, word2)
        levenshtein_apply = levenshtein_criteria(levenshtein_dist)
    else:
        levenshtein_apply = False

    return levenshtein_apply


def extract_drug_names(l, df_rxnconso):
    """
    Extract drug names from a list of words.

    :param l: list | List of words
    :param names: list | List of possible drug names
    :return: list | List of drug names in the list
    """
    extracted_names = []
    for x in tqdm.tqdm(l, desc="Tokens"):
        x_low = x.lower().strip()
        for el in df_rxnconso['low'].unique():
            are_equal = strict_equal_criteria(x_low, el)
            are_similar = metaphone_criteria(x_low, el)
            if are_equal:
                extracted_names.append((x_low, "true_eq"))
            elif are_similar:
                extracted_names.append((x_low, "meta_eq"))

    return extracted_names
