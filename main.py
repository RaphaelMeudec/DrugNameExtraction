"""Script for launching drug names extraction of a file."""
import nltk
import metaphone


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


if __name__ == "__main__":
    input_file = "file_modified.txt"
    tokens = text_file_to_tokens(input_file)
    clean_tokens = remove_stopwords(tokens)
    # TODO: drugs = rxnormhandler.list_drug_names()
    drugs = ['methadone', 'protonix', 'lovenox', 'azithromycin']

    drug_names = extract_drug_names(clean_tokens, drugs)
    print(drug_names)
