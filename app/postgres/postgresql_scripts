# Table that maps song-hash to song-name
CREATE TABLE hash_name (
  hash character varying(80),
  song_name character varying(150),
  CONSTRAINT persons_pkey PRIMARY KEY (hash)
);

# Load data into `hash_name`
\copy hash_name FROM '/path/to/file/hash_name.csv' with (format csv,header true, delimiter ',');

# Table that maps midi-instrument-code to instrument-name
CREATE TABLE midi_instrument(
	code VARCHAR (5) UNIQUE NOT NULL,
	name VARCHAR (80) NOT NULL,
	family VARCHAR (55) NOT NULL
);

\copy midi_instrument FROM '/path/to/file/midi_instruments.csv' with (format csv,header true, delimiter ',');
