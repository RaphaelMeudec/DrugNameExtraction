import pandas as pd
import metaphone


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
