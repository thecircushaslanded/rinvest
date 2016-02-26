from glob import glob

import pandas as pd

all_8k_files = []
for f in glob("*QTR*.csv"):
    df = pd.read_csv(f, sep=";", names=["form", "company", "CIK", "date", "path"])
    paths = df.path.tolist()
    all_8k_files.extend(paths)


already_downloaded = glob("0*.txt")
def is_already_downloaded(item):
    try: 
        already_downloaded.index(item)
    except ValueError:
        return False
    else:
        return True


file_and_path = [(path.split("/")[-1], "/".join(path.split("/")[:-1])) for path in all_8k_files]
file_and_path = [item for item in file_and_path if not is_already_downloaded(item[0])]

to_download = ["{},{}\n".format(item[1].split("/")[-1], item[0]) for item in file_and_path]
with open("8k_to_download.csv", 'w') as f:
    for line in to_download:
        f.write(line)

