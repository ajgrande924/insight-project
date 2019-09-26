# Script that reads a JSON file of all 170k songhash to songname. Script creates a corresponding CSV file hash_name.csv (used in `postgresql_scripts.py`)
import json, re, csv

# http://hog.ee.columbia.edu/craffel/lmd/md5_to_paths.json
with open('md5_to_paths.json') as json_file:
    data = json.load(json_file)

file_name_seq = []

for filehash,names in data.items():
    filename = filehash + '.mid'
    line1 = re.sub(r"\.mid$", "", names[0], flags=re.IGNORECASE)
    line2 = re.sub(r"[\_\-]", " ", line1)
    line3 = re.sub(r"\ {2,}"," ", line2)
    file_name_seq.append([filename, line3])

with open('assets/hash_names.csv', 'w') as file:
    header_names = ['filehash','name']
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerows([header_names])
    writer.writerows(file_name_seq)
