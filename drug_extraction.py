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


def extract_drug_names_from_rxnorm(df_rxnconso):
    """
    Extract list of drug names from the RXNORM Conso pd.DataFrame.

    :param df_rxnconso: pd.DataFrame | Dataframe of RXNORM CONSO table
    :return: set | List of drug names
    """
    df_names = df_rxnconso['STR']
    names = df_names.unique()
    # Removing all composed names as we split text on spaces
    names_low = set([name.lower().strip() for name in names if ' ' not in name.lower().strip()])

    return names_low


def strict_equal_criteria(word1, word2):
    """
    Test if two words are equal.

    :param word1: str | First word
    :param word2: str | Second word
    :return: boolean | Are they the same
    """
    return word1 == word2


def levenshtein_distance(word1, word2):
    """
    Compute the levenshtein distance between two words.

    :param word1: str | First word
    :param word2: str | Second word
    :return: float | Distance
    """
    size1, size2 = len(word1), len(word2)
    dist = np.zeros((size1+1, size2+1))
    dist[:, 0] = np.arange(size1+1)
    dist[0, :] = np.arange(size2+1)

    for i in range(1, size1+1):
        for j in range(1, size2+1):
            cout = 1 - (word1[i-1] == word2[j-1])
            dist[i, j] = min(dist[i-1, j] + 1, dist[i, j-1]+1, dist[i-1, j-1] + cout)

    return dist[size1, size2]


def levenshtein_criteria(distance, word):
    """
    Test if the distance is small enough in comparison to the word length.

    :param distance: float | Distance value
    :param word: str | Word that has been compared
    """
    length = len(word)
    if length == 0:
        return 0
    return distance/length < 0.2


def metaphone_criteria(word1, word2):
    """
    Apply a criteria based on metaphone comparison, and on resemblance between words.

    :param word1: str | First word
    :param word2: str | Second word
    :return: boolean | Are they close enough ?
    """
    word1_meta = metaphone.doublemetaphone(word1)
    word2_meta = metaphone.doublemetaphone(word2)
    metaphone_apply = word1_meta == word2_meta
    if metaphone_apply:
        levenshtein_dist = levenshtein_distance(word1, word2)
        levenshtein_apply = levenshtein_criteria(levenshtein_dist, word1)
    else:
        levenshtein_apply = False

    return levenshtein_apply


def are_words_close(word1, word2):
    """
    Apply strict equality test and then metaphone test to two words.

    :param word1: str | First word
    :param word2: str | Second word
    :return: str | Type of relation between words (true_eq, meta_eq, no_eq)
    """
    are_equal = strict_equal_criteria(word1, word2)
    if are_equal:
        return "true_eq"
    else:
        are_similar = metaphone_criteria(word1, word2)
        if are_similar:
            return "meta_eq"

    return "no_eq"


def is_word_in_list(word, drug_names):
    """
    Test if a word is related to words in a list.

    :param word: str | Word to test
    :param drug_names: list | List of drug names
    :return: str | If a word of the list is linked, returns the relation type ("true_eq", "meta_eq"), else return "no_eq"
    """
    word_low = word.lower().strip()
    for el in drug_names:
        relation = are_words_close(word_low, el)
        if relation != "no_eq":
            return relation

    return "no_eq"


def extract_drug_names(l, drug_names):
    """
    Extract drug names from a list of words.

    :param l: list | List of words
    :param names: list | List of possible drug names
    :return: list | List of drug names in the list
    """
    extracted_names = []
    for x in tqdm.tqdm(l, desc="Tokens"):
        relation = is_word_in_list(x, drug_names)
        if relation != "no_eq":
            extracted_names.append((x.lower().strip(), relation))

    return extracted_names
