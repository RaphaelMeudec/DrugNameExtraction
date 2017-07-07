"""Script for launching drug names extraction of a file."""
import os
import click
import file_preprocessing as fp
import drug_extraction as de


@click.command()
@click.option('--filepath', help="Path to file")
@click.option('--rxnormpath', default="rxnorm/", help="Path to the rxnorm directory containing the .csv")
@click.option('--verbose', default=1, help="Verbose")
def main(filepath, rxnormpath, verbose):
    if verbose:
        print("Setting paths to RXNORM.")
    RXNORM_PATH = rxnormpath
    RXNCONSO_PATH = os.path.join(RXNORM_PATH, "rxnconso.csv")

    if verbose:
        print("Loading file into tokens.")
    tokens = fp.text_file_to_tokens(filepath)
    if verbose:
        print("Remove stopwords from tokens.")
    clean_tokens = fp.remove_stopwords(tokens)

    rxnorm_paths = {
        'rxnconso': RXNCONSO_PATH
    }

    if verbose:
        print("Loading RXNORM.")
    df_rxnconso = de.load_rxnorm(rxnorm_paths)
    if verbose:
        print("Adding lower values and metaphone values")
    df_rxnconso = de.add_metaphone_to_rxnorm(df_rxnconso)
    if verbose:
        print("Extracting drug names from file.")
    drug_names = de.extract_drug_names(clean_tokens, df_rxnconso)
    if verbose:
        print("Done.")
        print(drug_names)


if __name__ == "__main__":
    main()
