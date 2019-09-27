import boto3
from io import BytesIO
import pretty_midi
import time

time_seq = []

time_seq.append(['start-read-midi', time.time()])
invalid_files = []
number_of_files = 0
number_of_valid_files = 0
filename_instruments_seq = []

# Set s3-boto config
s3_bucket = 'lmd-midi'
s3 = boto3.resource('s3')
boto_client = boto3.client('s3')
bucket = s3.Bucket(s3_bucket)

# stores (filename, list(instrument))
filename_instruments_seq = []

# stores (filename, instrument) This is denormalized format of above. 
# A filename will have an entry for each instrument.
filename_instrument_seq = []

for obj in bucket.objects.all():
    print(obj.key)
    number_of_files += 1
    s3_key = obj.key
    midi_obj_stream = boto_client.get_object(Bucket=s3_bucket, Key=s3_key)
    midi_obj = BytesIO(midi_obj_stream['Body'].read())
    try:
        print('try midi')
        # Try required as a few MIDI files are invalid.
        pretty_midi_obj = pretty_midi.PrettyMIDI(midi_obj)
        number_of_valid_files += 1
        filename = s3_key
        instruments_list = list(map(lambda x: str(x.program), pretty_midi_obj.instruments))
        instruments_list_set = set(instruments_list)
        instruments_list_uniq = list(instruments_list_set)
    except:
        print('invalid midi')
        # Invalid MIDI files are stored.
        invalid_files.append(s3_key)
    time_seq.append(['end read-file', time.time()])