import numpy as np
import pymysql.cursors


class RxNormHandler:
    def __init__(self):
        self.USERNAME="root"
        self.PASSWORD="root"
        self.HOST="localhost"
        self.DATABASE="rxnorm"

    def connect(self):
        pass

def extract_drug_names(tokens):
    pass

if __name__=="__main__":
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="bios",
        db="rxnorm",
        charset="utf8",
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT * FROM `RXNREL` WHERE `email`=%s"
            cursor.execute(sql, ('webmaster@python.org',))
            result = cursor.fetchone()
            print(result)
    finally:
        connection.close()
