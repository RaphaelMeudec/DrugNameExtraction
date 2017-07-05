import nltk


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
