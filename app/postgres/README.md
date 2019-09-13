## Setup Info
This folder contains the scripts that were run to setup a few PostgreSQL tables. These tables are used in Flask app.

The scripts were run in the order:

```sh
# generate md5_to_paths.json
curl http://hog.ee.columbia.edu/craffel/lmd/md5_to_paths.json > md5_to_paths.json

# generate hash_name.csv
python3 create_midi_instrument_csv.py

# Run each line in PostgreSQL shell
./postgresql_scripts
```
