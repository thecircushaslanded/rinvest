import re
import ftplib
import pickle as pkl
from collections import Counter
from glob import glob
from os.path import isfile
from os import chdir
from subprocess import call
from itertools import product

import pandas as pd

chdir("txt")
already_downloaded = glob("0*.txt")

def is_interesting_file(txt_file):
    """ 
    Determines if the file documents an Unregistered sale of equities.
    """ 
    with open(txt_file, 'r') as f:
        items = re.findall(r"^ITEM INFORMATION:.*", "".join(f.readlines(2048)), flags=re.MULTILINE)
    try:
        items.index("ITEM INFORMATION:\t\tUnregistered Sales of Equity Securities")
    except ValueError:
        call(['rm', txt_file])
        previously_downloaded.append(txt_file)
        return False
    else:
        if "discount" in open(txt_file, 'r').read():
            return True
        else:
            return False

previously_downloaded = pkl.load(open("../previous.pkl", 'r'))
interesting_files = [f for f in already_downloaded if is_interesting_file(f)]
pkl.dump(previously_downloaded, open("../previous.pkl", 'w'))


def extract_basic_data(txt_file):
    items = []
    url = "https://www.sec.gov/cgi-bin/srch-edgar?text=ACCESSION-NUMBER%3D{}&first=2010&last=2016".format(
            txt_file[:-4])
    items.append(url)
    # for s in [r"		COMPANY CONFORMED NAME:*", r"FILED AS OF DATE:*:", r"^ITEM INFORMATION:.*"]:
    for s in [r"COMPANY CONFORMED NAME:.*$", r"FILED AS OF DATE:.*$", r"ITEM INFORMATION:.*"]:
        with open(txt_file, 'r') as f:
            items.extend(re.findall(s, f.read(), flags=re.MULTILINE))
    return ";".join(items).replace('\t', ' ')

basic_data = [extract_basic_data(f) for f in interesting_files]
basic_data_str = '\n'.join(basic_data)
basic_data_str = basic_data_str.replace("COMPANY CONFORMED NAME:", "")
basic_data_str = basic_data_str.replace("FILED AS OF DATE:", "")
basic_data_str = basic_data_str.replace("ITEM INFORMATION:", "")
with open("../SelectedFilings.csv", 'w') as f:
    f.write(basic_data_str)
print(len(basic_data))

company_names = [i.split(";")[0] for i in basic_data]
duplicates = [item for item, count in Counter(company_names).items() if count > 1]



