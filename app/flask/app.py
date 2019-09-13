from flask import Flask, send_file, jsonify, session, request
import psycopg2
import config
import json
import re

app = Flask(__name__)
app.secret_key = config.APP_SECRET_KEY

@app.route("/")
def index():
    return send_file('index.html')

@app.route("/show_similar_songs/<filename>")
def show_similar_songs(filename):
    session['filename'] = filename
    return send_file('show_similar_songs.html')

@app.route("/load_index.js")
def load_index_js():
    return send_file('load_index.js')

@app.route("/load_similar_songs.js")
def load_similar_songs_js():
    return send_file('load_similar_songs.js')

def get_10songs_for_instrument(cursor,instrument_code):
    query = 'SELECT song_name,fi.filename ' + \
            '  FROM filename_instrument_run3 fi ' + \
            '  JOIN hash_name hn ON hn.hash = fi.filename ' + \
            ' WHERE fi.instrument =  \'' + str(instrument_code) + '\' ' + \
            ' LIMIT 10;'
    cursor.execute(query)
    songnames = list(map(lambda x: [ clean_text(x[0]), x[1]], cursor))
    return songnames

@app.route("/load_index")
def load_index_page():
    with psycopg2.connect(dbname=config.PGSQL_DBNAME, user=config.PGSQL_USER, password=config.PGSQL_PASSWORD, host=config.PGSQL_HOST, port=config.PGSQL_PORT) as conn:
        with conn.cursor() as cur:
            songs_by_instrument = {
                'Electric Grand Piano': get_10songs_for_instrument(cur, 2),
                'Violin': get_10songs_for_instrument(cur, 40),
                'String Ensemble 1': get_10songs_for_instrument(cur, 48),
                'Clarinet': get_10songs_for_instrument(cur, 71),
                'Flute': get_10songs_for_instrument(cur, 73),
                'Bag pipe': get_10songs_for_instrument(cur, 109),
                'Steel Drums': get_10songs_for_instrument(cur, 114)
            }
    cur.close()
    conn.close()
    return jsonify(songs_by_instrument)

@app.route("/get_similar_songs")
def get_similar_songs():
    filename = session['filename']
    conn = psycopg2.connect(dbname=config.PGSQL_DBNAME, user=config.PGSQL_USER, password=config.PGSQL_PASSWORD, host=config.PGSQL_HOST, port=config.PGSQL_PORT)
    cur1 = conn.cursor()
    query = 'SELECT similar_song_filename, hn.song_name, similarity_score, COUNT(fi.instrument), array_agg(fi.instrument) ' + \
            '  FROM ( ' + \
            '	 SELECT (1 - distance) AS similarity_score, ' +\
            '        CASE WHEN fs."filename_A" = \'' + filename + '\' THEN "filename_B" ' + \
            ' 	          ELSE fs."filename_A" ' + \
            '	   	 END AS similar_song_filename ' + \
            '	  FROM filepair_similarity_run3 fs ' + \
            '	 WHERE ("filename_A" = \'' + filename +'\' ' + \
            ' 		     OR "filename_B" = \'' + filename + '\' ) ' + \
            '	 ORDER BY distance ' + \
            ' 	 ) AS tbl1 ' + \
            'JOIN hash_name hn ON hn.hash = tbl1.similar_song_filename ' + \
            'JOIN filename_instrument_run3 fi ON fi.filename = similar_song_filename ' + \
            'GROUP BY similar_song_filename, hn.song_name, similarity_score;'
    cur1.execute(query)
    similar_songnames = list(map(lambda x: { 'filename': x[0], 'songname': clean_text(x[1]),
                                    'similarity': x[2], 'num_of_inst': x[3], 'instrument_code': x[4] }, cur1))
    cur1.close()
    cur2 = conn.cursor()
    query2 ='SELECT hn.hash, hn.song_name, array_agg(fi.instrument) ' + \
            '  FROM filename_instrument_run3 fi ' + \
            '  JOIN hash_name hn ON hn.hash = \'' + filename + '\' ' + \
            ' WHERE filename = \'' + filename + '\' ' + \
            ' GROUP BY hn.hash'
    cur2.execute(query2)
    song_info = list(map(lambda x: { 'filename': x[0], 'songname': clean_text(x[1]),
                                     'instruments': x[2]}, cur2 ))

    conn.close()
    respObj = { 'song_info': song_info, 'similar_songs': similar_songnames }
    return jsonify(respObj)

@app.route("/get_songs_for_instruments", methods=['GET', 'POST'])
def get_songs_for_instruments():
    if request.method == 'POST':
        content = request.json
        instrument = content['instruments']
        query = 'SELECT fi.filename, hn.song_name, COUNT(DISTINCT fi.instrument) num_of_instruments, ' + \
                '       COUNT(fs.distance) / COUNT(DISTINCT fi.instrument) AS num_of_simSongs ' + \
                'FROM ( ' + \
                '       SELECT filename ' + \
                '       FROM filename_instrument_run3 ' + \
                '       WHERE instrument = \'' + instrument + '\' ' + \
                ' ) tbl ' + \
                'JOIN hash_name hn ON hn.hash = tbl.filename ' + \
                'JOIN filename_instrument_run3 fi ON fi.filename = tbl.filename ' + \
                'JOIN filepair_similarity_run3 fs ON (fs."filename_A" = tbl.filename OR fs."filename_B" = tbl.filename ) ' + \
                'GROUP BY fi.filename, hn.song_name;'
        conn = psycopg2.connect(dbname=config.PGSQL_DBNAME, user=config.PGSQL_USER, password=config.PGSQL_PASSWORD, host=config.PGSQL_HOST, port=config.PGSQL_PORT)
        cur = conn.cursor()
        cur.execute(query)
        filenames = list(map(lambda x: {'filename': x[0], 'song_name': clean_text(x[1]), 'num_of_inst': x[2], 'num_of_simSongs': x[3] }, cur))
        cur.close()
        conn.close()
        return jsonify(filenames)

def clean_text(txt):
    return re.sub('[^A-Za-z0-9\']+', ' ', txt).lower().title()

if __name__ == "__main__":
    app.run(port="80", host="0.0.0.0")
