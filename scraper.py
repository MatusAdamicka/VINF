import requests
import time
import csv
from bs4 import BeautifulSoup
from csv import DictWriter
from csv import writer
import numpy as np
import pandas as pd

# ------------------------------------------------


def get_content(url):
    page = requests.get(url)
    return BeautifulSoup(page.content.decode("utf-8"), features="html.parser")


def save_to_file(content, mode, filename, encoding):
    f = open(filename, mode, encoding=encoding)
    f.write(content)
    f.close()


def truncate_file(filename):
    f = open(OUTPUT_FILENAME, "w+")
    f.truncate()
    f.close()


def load_fieldnames(filename):
    f = open(filename, "r")
    field_names = f.read().splitlines()
    return field_names


# ------------------------------------------------

OUTPUT_FILENAME = "drugs1.csv"
URL_PREFIX = "https://go.drugbank.com/drugs/DB"
DRUGS = []

truncate_file(OUTPUT_FILENAME)
# FIELDS = load_fieldnames("field_names.txt")
FIELDS = ["Name"]

for URL_SUFFIX in range(1, 50):

    # generate url
    url = URL_PREFIX + (5 - len(str(URL_SUFFIX))) * "0" + str(URL_SUFFIX)
    print(url)

    # get html content
    html = get_content(url)

    # get name attribute
    attributes = {"Name": html.find(class_='content-header d-sm-flex align-items-center').text}

    # get other attributes
    for myparent in html.find(class_='card-content px-md-4 px-sm-2 pb-md-4 pb-sm-2').find_all("dl"):
        for mychild in myparent.find_all("dt"):
            col = mychild.text.strip()
            if col not in FIELDS: FIELDS.append(col)
            # if col not in FIELDS: continue
            val = mychild.find_next('dd').text.strip().replace('\n', '').replace('  ', '')
            attributes[col] = val

    # save to array
    DRUGS.append(attributes)

    # print
    # print("{" + "\n".join("{!r}: {!r},".format(k, v) for k, v in attributes.items()) + "}")

    # wait
    time.sleep(30)

# save array to file
csvf = open("drugs.csv", "a+", newline='', encoding="utf-8")
writerobj = DictWriter(csvf, fieldnames=FIELDS)
writerobj.writeheader()
for drug in DRUGS:
    writerobj.writerow(drug)
csvf.close()
