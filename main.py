"""Script for launching drug names extraction of a file."""
import os
import pandas as pd
import nltk
import metaphone
import click


def text_file_to_tokens(filepath):
    """
    Transform file into tokens.

    :param filepath: str | Path to file
    :return: list | Tokenized words
    """
    f = open(filepath, 'r')
    txt = f.read()
    f.close()
    return nltk.word_tokenize(txt)


def remove_stopwords(tokens, ponct=True, language="english"):
    """
    Remove stopwords from a list of words.

    :param tokens: list | List of words to examine
    :param ponct: bool | Remove ponctuation ?
    :param language: str | language of the words
    :return: list | List of words filtered
    """
    stop = set(nltk.corpus.stopwords.words(language))
    if ponct:
        stop.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}'])
    l = []
    for token in tokens:
        if token.lower().strip() not in stop:
            l.append(token)
    return l


def generate_list_of_drugs(paths):
    """
    Generate list of drug names based on rxnorm database.

    :param paths: dict | Dictionnary of path with table names as keys
    :return: pd.DataFrame | Data
    """
    rxnconso_df = pd.read_csv(paths['rxnconso'])
    rxnrel_df = pd.read_csv(paths['rxnrel'])
    return rxnconso_df, rxnrel_df


def extract_drug_names(l, names):
    """
    Extract drug names from a list of words.

    :param l: list | List of words
    :param names: list | List of possible drug names
    :return: list | List of drug names in the list
    """
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


@click.command()
@click.option('--filepath', help="Path to file")
@click.option('--rxnormpath', help="Path to the rxnorm directory containing the .csv")
def main(filepath, rxnormpath):
    RXNORM_PATH = rxnormpath
    RXNCONSO_PATH = os.path.join(RXNORM_PATH, "rxnconso.csv")
    RXNREL_PATH = os.path.join(RXNORM_PATH, "rxnrel.csv")
    RXNSAB_PATH = os.path.join(RXNORM_PATH, "rxnsab.csv")
    RXNSAT_PATH = os.path.join(RXNORM_PATH, "rxnsat.csv")
    RXNSTY_PATH = os.path.join(RXNORM_PATH, "rxnsty.csv")

    tokens = text_file_to_tokens(filepath)
    clean_tokens = remove_stopwords(tokens)

    rxnorm_paths = {
        'rxnconso': RXNCONSO_PATH,
        'rxnrel': RXNREL_PATH,
        'rxnsab': RXNSAB_PATH,
        'rxnsat': RXNSAT_PATH,
        'rxnsty': RXNSTY_PATH
    }

    drugs = ['methadone', 'protonix', 'lovenox', 'azithromycin']
    # drugs = generate_list_of_drugs(rxnorm_paths)

    drug_names = extract_drug_names(clean_tokens, drugs)
    print(drug_names)


if __name__ == "__main__":
    main()
