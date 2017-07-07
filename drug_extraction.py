import pandas as pd
import metaphone
import tqdm


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
        x_meta = metaphone.doublemetaphone(x_low)
        if x_low in df_rxnconso['low'].unique():
            extracted_names.append((x_low, "true_eq"))
        else:
            for el in df_rxnconso['dmeta'].unique():
                if (el == x_meta) & (len(el[0]) > 1):
                    extracted_names.append((x_low, "meta_eq"))

    return extracted_names
