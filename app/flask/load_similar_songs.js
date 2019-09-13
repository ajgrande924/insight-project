$(document).ready(function(){
  load_similar_songs();
});

function load_similar_songs() {
  $.get("/get_similar_songs", function(data, status){
    var ins_in_base_song_obj = {};
    for(var i in data.song_info[0].instruments) {
      var ins_code = data.song_info[0].instruments[i];
      var ins_name = midi_instrument[ins_code];
      ins_in_base_song_obj[ins_code] = ins_name;
    }
    var ins_in_base_song = _.values(ins_in_base_song_obj);
    $('#base_song_name').html(data.song_info[0].songname);
    $('#base_song_num_of_ins').html(ins_in_base_song.length);
    $('#base_song_ins').html(ins_in_base_song.join(', '));
    var dataSet = data.similar_songs.map(function(a) {
      var similarity_score = Math.round(a.similarity * 100) / 100;
      var num_of_shared_instruments = 0;
      var ins_in_song = [];
      var instrument_names = a.instrument_code.map(function(code) {
        var ins_name = midi_instrument[code];
        ins_in_song.push(ins_name);
        var ins_name_html;
        if (ins_in_base_song_obj[code]) {
          ins_name_html = "<span class=\"ins_present\">" + ins_name + "</span>";
          num_of_shared_instruments++;
        } else {
          ins_name_html = ins_name;
        }
        return ins_name_html;
      });
      var ins_uniq = _.uniq(ins_in_song.concat(ins_in_base_song)),
          ins_uniq_count = ins_uniq.length;
      var computed_similarity_score =  Math.round((num_of_shared_instruments / ins_uniq_count) * 100) / 100;
      return [a.songname, similarity_score, a.num_of_inst, num_of_shared_instruments, instrument_names];
    });
    $('#similar_songs_table').DataTable( {
      data: dataSet,
      columns: [  { title: "Song Name" },
                  { title: "Similarity Score" },
                  { title: "Num of Instruments" },
                  { title: "Num of Shared Instruments" },
                  { title: "Instruments (Shared Instruments shown in <span class=\"ins_present\">green</span>)" }],
      "order": [[ 1, "desc" ]],
      "language": {
          "lengthMenu": "Show _MENU_ songs",
          "zeroRecords": "No songs to show",
          "info": "Showing _START_ to _END_ of _TOTAL_ songs",
          "infoEmpty":      "No songs",
          "infoFiltered":   "(filtered from _MAX_ songs)"
      }
    });
  });
}

var midi_instrument = {
  "0":"Acoustic Grand Piano",
  "1":"Bright Acoustic Piano",
  "2":"Electric Grand Piano",
  "3":"Honky-tonk Piano",
  "4":"Electric Piano 1",
  "5":"Electric Piano 2",
  "6":"Harpsichord",
  "7":"Clavi",
  "8":"Celesta",
  "9":"Glockenspiel",
  "10":"Music Box",
  "11":"Vibraphone",
  "12":"Marimba",
  "13":"Xylophone",
  "14":"Tubular Bells",
  "15":"Dulcimer",
  "16":"Drawbar Organ",
  "17":"Percussive Organ",
  "18":"Rock Organ",
  "19":"Church Organ",
  "20":"Reed Organ",
  "21":"Accordion",
  "22":"Harmonica",
  "23":"Tango Accordion",
  "24":"Acoustic Guitar (nylon)",
  "25":"Acoustic Guitar (steel)",
  "26":"Electric Guitar (jazz)",
  "27":"Electric Guitar (clean)",
  "28":"Electric Guitar (muted)",
  "29":"Overdriven Guitar",
  "30":"Distortion Guitar",
  "31":"Guitar harmonics",
  "32":"Acoustic Bass",
  "33":"Electric Bass (finger)",
  "34":"Electric Bass (pick)",
  "35":"Fretless Bass",
  "36":"Slap Bass 1",
  "37":"Slap Bass 2",
  "38":"Synth Bass 1",
  "39":"Synth Bass 2",
  "40":"Violin",
  "41":"Viola",
  "42":"Cello",
  "43":"Contrabass",
  "44":"Tremolo Strings",
  "45":"Pizzicato Strings",
  "46":"Orchestral Harp",
  "47":"Timpani",
  "48":"String Ensemble 1",
  "49":"String Ensemble 2",
  "50":"SynthStrings 1",
  "51":"SynthStrings 2",
  "52":"Choir Aahs",
  "53":"Voice Oohs",
  "54":"Synth Voice",
  "55":"Orchestra Hit",
  "56":"Trumpet",
  "57":"Trombone",
  "58":"Tuba",
  "59":"Muted Trumpet",
  "60":"French Horn",
  "61":"Brass Section",
  "62":"SynthBrass 1",
  "63":"SynthBrass 2",
  "64":"Soprano Sax",
  "65":"Alto Sax",
  "66":"Tenor Sax",
  "67":"Baritone Sax",
  "68":"Oboe",
  "69":"English Horn",
  "70":"Bassoon",
  "71":"Clarinet",
  "72":"Piccolo",
  "73":"Flute",
  "74":"Recorder",
  "75":"Pan Flute",
  "76":"Blown Bottle",
  "77":"Shakuhachi",
  "78":"Whistle",
  "79":"Ocarina",
  "80":"Lead 1 (square)",
  "81":"Lead 2 (sawtooth)",
  "82":"Lead 3 (calliope)",
  "83":"Lead 4 (chiff)",
  "84":"Lead 5 (charang)",
  "85":"Lead 6 (voice)",
  "86":"Lead 7 (fifths)",
  "87":"Lead 8 (bass + lead)",
  "88":"Pad 1 (new age)",
  "89":"Pad 2 (warm)",
  "90":"Pad 3 (polysynth)",
  "91":"Pad 4 (choir)",
  "92":"Pad 5 (bowed)",
  "93":"Pad 6 (metallic)",
  "94":"Pad 7 (halo)",
  "95":"Pad 8 (sweep)",
  "96":"FX 1 (rain)",
  "97":"FX 2 (soundtrack)",
  "98":"FX 3 (crystal)",
  "99":"FX 4 (atmosphere)",
  "100":"FX 5 (brightness)",
  "101":"FX 6 (goblins)",
  "102":"FX 7 (echoes)",
  "103":"FX 8 (sci-fi)",
  "104":"Sitar",
  "105":"Banjo",
  "106":"Shamisen",
  "107":"Koto",
  "108":"Kalimba",
  "109":"Bag pipe",
  "110":"Fiddle",
  "111":"Shanai",
  "112":"Tinkle Bell",
  "113":"Agogo",
  "114":"Steel Drums",
  "115":"Woodblock",
  "116":"Taiko Drum",
  "117":"Melodic Tom",
  "118":"Synth Drum",
  "119":"Reverse Cymbal",
  "120":"Guitar Fret Noise",
  "121":"Breath Noise",
  "122":"Seashore",
  "123":"Bird Tweet",
  "124":"Telephone Ring",
  "125":"Helicopter",
  "126":"Applause",
  "127":"Gunshot"
};
