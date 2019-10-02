\c lmd
\copy hash_name FROM '/tmp/hash_names.csv' with (format csv,header true, delimiter ',');
\copy midi_instrument FROM '/tmp/midi_instruments.csv' with (format csv,header true, delimiter ',');
