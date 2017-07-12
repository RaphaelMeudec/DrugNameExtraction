"""Script for launching drug names extraction of a file."""
import os
import click
import file_preprocessing as fp
import drug_extraction as de
import logging

LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL}


@click.command()
@click.option('--filepath', help="Path to file")
@click.option('--rxnormpath', default="rxnorm/", help="Path to the rxnorm directory containing the .csv")
@click.option('--verbose', default='info', help="Logging level (debug, info, warning, error, critical)")
def extract_drug_names(filepath, rxnormpath, verbose):
    logging.basicConfig(level=LEVELS[verbose])

    logging.info("Setting paths to RXNORM.")
    RXNORM_PATH = rxnormpath
    RXNCONSO_PATH = os.path.join(RXNORM_PATH, "rxnconso.csv")

    logging.info("Loading file into tokens.")
    tokens = fp.text_file_to_tokens(filepath)
    logging.info("Remove stopwords from tokens.")
    clean_tokens = fp.remove_stopwords(tokens)

    rxnorm_paths = {
        'rxnconso': RXNCONSO_PATH
    }

    logging.info("Loading RXNORM.")
    df_rxnconso = de.load_rxnorm(rxnorm_paths)
    logging.info("Adding lower values and metaphone values")
    drug_names_list = de.extract_drug_names_from_rxnorm(df_rxnconso)
    logging.info("Extracting drug names from file.")
    drug_names = de.extract_drug_names(clean_tokens, drug_names_list)
    logging.info("Done.")
    print(drug_names)


def compare_tuheeg_file(filepath, rxnormpath, verbose):
    print(filepath, rxnormpath, verbose)
    logging.basicConfig(level=LEVELS[verbose])

    logging.info("Setting paths to RXNORM.")
    RXNORM_PATH = rxnormpath
    RXNCONSO_PATH = os.path.join(RXNORM_PATH, "rxnconso.csv")

    logging.info("Loading file into tokens")
    tokens = fp.text_file_to_tokens(filepath)
    logging.info("Remove stopwords from tokens.")
    clean_tokens = fp.remove_stopwords(tokens)

    rxnorm_paths = {
        'rxnconso': RXNCONSO_PATH
    }

    logging.info("Loading RXNORM.")
    df_rxnconso = de.load_rxnorm(rxnorm_paths)
    logging.info("Drug names extraction from rxnorm")
    drug_names_list = de.extract_drug_names_from_rxnorm(df_rxnconso)
    logging.info("Extracting drug names from file.")
    drug_names = de.extract_drug_names(clean_tokens, drug_names_list)
    logging.info("Parsing TUHEEG file")
    drug_names_real = fp.parse_tuheeg_drug_names(filepath)

    print(drug_names)
    print(drug_names_real)


@click.command()
@click.option('--dirpath', default="tuheeg/", help="Path to directory of .txt files")
@click.option('--rxnormpath', default="rxnorm/", help="Path to the rxnorm directory")
@click.option('--verbose', default="info")
def compare_tuheeg(dirpath, rxnormpath, verbose):
    for filename in os.listdir(dirpath):
        path = os.path.join(dirpath, filename)
        compare_tuheeg_file(path, rxnormpath, verbose)


if __name__ == "__main__":
    compare_tuheeg()
