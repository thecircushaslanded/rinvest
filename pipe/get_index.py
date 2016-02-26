
import re
import ftplib
from glob import glob
from os.path import isfile
from subprocess import call
from itertools import product

import pandas as pd


years = range(2010,2015+1, 1)
qtrs = ["QTR1", "QTR2", "QTR3", "QTR4"] 

for year, q in product(years, qtrs):
    if ~isfile("qtr/{}{}.csv".format(year, q)):
        print year, q
        form = "/edgar/full-index/"+str(year)+"/"+q
        ftp = ftplib.FTP("ftp.sec.gov") 
        ftp.login("anonymous", "thecircushaslanded@gmail.com") 
        ftp.cwd(form)
        ftp.retrbinary("RETR " + "form.zip", open("{}{}.zip".format(year, q), 'wb').write)
        ftp.quit()
        call(["rm", "form.idx"])
        call(["unzip", "{}{}.zip".format(year, q)])
        call(["rm", "{}{}.zip".format(year, q)])

        with open("form.idx", "rb") as f:
            strings = re.findall(r"^8-K.*", f.read(), flags=re.MULTILINE)
        with open("{}{}.csv".format(year, q), 'w') as f:
            for s in strings: 
                new_s = s[:11].strip()+';'+s[12:74].strip()+';'+s[75:86].strip()+\
                            ';'+s[86:97].strip()+';'+s[98:].strip()+"\n"
                f.write(new_s+"\n")

