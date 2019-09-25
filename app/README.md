## Setup Info

### s3 + spark

```sh
# in app/
wget http://hog.ee.columbia.edu/craffel/lmd/lmd_full.tar.gz
tar -xvzf lmd_full.tar.gz
aws s3 cp lmd_full s3://lmd-midi --recursive
```

### postgres

This folder contains the scripts that were run to setup a few PostgreSQL tables. These tables are used in Flask app.

The scripts were run in the order:

```sh
# generate md5_to_paths.json
curl http://hog.ee.columbia.edu/craffel/lmd/md5_to_paths.json > md5_to_paths.json

# generate hash_names.csv
python3 create_midi_instrument_csv.py

# Run each line in PostgreSQL shell
./postgresql_scripts
```
