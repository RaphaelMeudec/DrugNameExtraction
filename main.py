"""Script for launching drug names extraction of a file."""
import os
import click
import file_preprocessing as fp
import drug_extraction as de


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

    tokens = fp.text_file_to_tokens(filepath)
    clean_tokens = fp.remove_stopwords(tokens)

    rxnorm_paths = {
        'rxnconso': RXNCONSO_PATH,
        'rxnrel': RXNREL_PATH,
        'rxnsab': RXNSAB_PATH,
        'rxnsat': RXNSAT_PATH,
        'rxnsty': RXNSTY_PATH
    }

    drugs = ['methadone', 'protonix', 'lovenox', 'azithromycin']
    # drugs = de.generate_list_of_drugs(rxnorm_paths)

    drug_names = de.extract_drug_names(clean_tokens, drugs)
    print(drug_names)


if __name__ == "__main__":
    main()
