import re
import ftplib
import pickle as pkl
from collections import Counter
from glob import glob
from os.path import isfile
from subprocess import call
from itertools import product

import pandas as pd

all_df = []
for f in glob("qtr/*QTR*.csv"):
    df = pd.read_csv(f, sep=";", names=["form", "company", "CIK", "date", "path"])
    all_df.append(df)

df = pd.concat(all_df)

df["file"] =  [path.split("/")[-1] for path in df.path]
df["path"] =  ["/".join(path.split("/")[:-1]) for path in df.path]
# already_downloaded = glob("0*.txt")
already_downloaded = pkl.load(open("previous.pkl", 'r'))

df = df[~df["file"].isin(already_downloaded)]

def download_files(gb):
    ftp = ftplib.FTP("ftp.sec.gov") 
    ftp.login("anonymous", "thecircushaslanded@gmail.com") 
    ftp_dir = gb["path"].tolist()[0]
    ftp.cwd(ftp_dir)
    for f in gb["file"].tolist():
        try:
            ftp.retrbinary("RETR " + f, open("txt/"+f, 'wb').write)
            already_downloaded.append(f)
            print f
        except:
            print "Error."
    ftp.quit()

df.groupby("CIK").apply(download_files)

#  find . -size  0 -print0 |xargs -0 rm

interesting_files = [f for f in glob("txt/0*txt") if is_interesting_file(f)]
def is_interesting_file(txt_file):
    """ 
    Determines if the file documents an Unregistered sale of equities.
    """ 
    with open(txt_file, 'r') as f:
        items = re.findall(r"^ITEM INFORMATION:.*", f.readlines(2048), flags=re.MULTILINE)
    try:
        items.index("ITEM INFORMATION:\t\tUnregistered Sales of Equity Securities")
    except ValueError:
        return False
    else:
        if "discount" in open(txt_file, 'r').read():
            return True
        else:
            return True # we'll not filter on this just yet.



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

