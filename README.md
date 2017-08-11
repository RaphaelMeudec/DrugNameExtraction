# Drug Name Extraction

This project aims at extracting from a text file the words that match drug names. It can be useful when, given a patient record, you want to extract the information about the drug use. It is based on the following paper.

```
@inproceedings{levin2007extraction,
  title={Extraction and mapping of drug names from free text to a standardized nomenclature},
  author={Levin, Matthew A and Krol, Marina and Doshi, Ankur M and Reich, David L},
  booktitle={AMIA Annual Symposium Proceedings},
  volume={2007},
  pages={438},
  year={2007},
  organization={American Medical Informatics Association}
}
``` 

# Installation

Packages required are in the `requirements.txt` file. You can simply init a virtual environment and install the packages with :

```
virtual venv -p python3
pip install -r requirements.txt
```

# RxNORM

This project is based on the RxNORM database, by the U.S National Library of Medicine. Make sure you get the sql tables from their website, and export them as csv files in a `rxnorm` directory.

# Use

To run the analysis, just use:
```python
python main.py --dirpath=path/to/my/file.txt --rxnormpath=path/to/rxnorm
```
