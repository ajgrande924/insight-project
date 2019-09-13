from pyspark.sql import *
import pyspark.sql.functions as f
from pyspark import SparkConf
from pyspark import SparkContext
from pyspark.ml import Pipeline
from pyspark.ml.feature import RegexTokenizer, NGram, HashingTF, MinHashLSH

from io import BytesIO

import boto3
import pretty_midi
import os
import sys
import time

s3_bucket = 'midi-files-sample2'  # 11258

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/lib")
import config

time_seq = []

#Define Spark Configuration
def spark_conf():
    conf = SparkConf().setAppName("processMIDIfiles")
    sc = SparkContext(conf=conf)
    spark = SparkSession.builder.getOrCreate()
    return spark

spark = spark_conf()

#Function to write spark-dataframe to PostgreSQL
def write_df_to_pgsql(df, table_name):
    postgresql_user = os.environ.get('POSTGRESQL_USER')
    postgresql_password = os.environ.get('POSTGRESQL_PWD')
    df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://10.0.0.13:2762/lmd") \
        .option("dbtable", table_name) \
        .option("user", postgresql_user) \
        .option("password", postgresql_password) \
        .save()

#Compute Similarity Score for song pairs
def process_df(df):
    time_seq.append(['start process-df', time.time()])
    model = Pipeline(stages = [RegexTokenizer(pattern = " ", inputCol = "instruments", outputCol = "instruments_tokenized", minTokenLength = 1),
                           NGram(n = 1, inputCol = "instruments_tokenized", outputCol = "instruments_ngrams"),
                           HashingTF(inputCol = "instruments_ngrams", outputCol = "instruments_vectors"),
                           MinHashLSH(inputCol = "instruments_vectors", outputCol = "instruments_lsh", numHashTables = 10)]).fit(df)

    df_hashed = model.transform(df)
    df_matches = model.stages[-1].approxSimilarityJoin(df_hashed, df_hashed, 0.5, distCol="distance") \
        .filter("datasetA.filename != datasetB.filename AND datasetA.filename < datasetB.filename") \
        .select(f.col('datasetA.filename').alias('filename_A'),
                f.col('datasetB.filename').alias('filename_B'),
                f.col('distance'))
    time_seq.append(['process-df df_matches', time.time()])
    write_df_to_pgsql(df_matches, 'filepair_similarity_run3')
    time_seq.append(['write pgsql', time.time()])
    print('time_seq', time_seq)

#Read all MIDI files from S3 bucket
def read_midi_files():
    time_seq.append(['start-read-midi', time.time()])
    invalid_files = []
    number_of_files = 0
    number_of_valid_files = 0
    filename_instruments_seq = []

    #Set s3-boto config
    s3 = boto3.resource('s3')
    boto_client = boto3.client('s3')
    bucket = s3.Bucket(s3_bucket)

    # DataFrame schema
    File_Instruments = Row("filename", "instruments")
    Filename_Instrument = Row("filename", "instrument")
    # stores (filename, list(instrument))
    filename_instruments_seq = []
    # stores (filename, instrument) This is denormalized format of above. A filename will have an entry for each instrument.
    filename_instrument_seq = []

    # Read each MIDI file from AWS S3 bucket
    for obj in bucket.objects.all():
        number_of_files+=1
        s3_key = obj.key
        midi_obj_stream = boto_client.get_object(Bucket=s3_bucket, Key=s3_key)
        midi_obj = BytesIO(midi_obj_stream['Body'].read())
        try:
            # Try required as a few MIDI files are invalid.
            pretty_midi_obj = pretty_midi.PrettyMIDI(midi_obj)
            number_of_valid_files+=1
            filename = s3_key
            instruments_list = list(map(lambda x: str(x.program), pretty_midi_obj.instruments))
            instruments_list_set = set(instruments_list)
            instruments_list_uniq = list(instruments_list_set)
            for instrument in instruments_list_uniq:
                filename_instrument_seq.append(Filename_Instrument(filename, instrument))
            instruments_str = " ".join(instruments_list_uniq)
            if(len(instruments_list_uniq) >=3):
                filename_instruments_seq.append(File_Instruments(filename,instruments_str))
        except:
            # Invalid MIDI files are stored.
            invalid_files.append(s3_key)
    time_seq.append(['end read-file', time.time()])
    df_filename_instrument = spark.createDataFrame(filename_instrument_seq)
    write_df_to_pgsql(df_filename_instrument, 'filename_instrument_run3')
    df_song_instrument = spark.createDataFrame(filename_instruments_seq)
    process_df(df_song_instrument)

if __name__ == '__main__':
    time_seq.append(['start', time.time()])
    read_midi_files()
