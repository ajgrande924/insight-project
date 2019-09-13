$(document).ready(function(){
  $("#instruments").select2({
    placeholder: 'Select/search 1 instrument',
    allowClear: true
  });
  $('#instruments').on('select2:select', function (e) {
    var instruments = $('#instruments').val();
    fetch_songs_for_instruments(instruments);
  });
});

function fetch_songs_for_instruments(instruments) {
  var postObj = { 'instruments': instruments };
  var success = function(data,status) {
    var data_song = data.map(function(a) {
      var link_to_similarSongs = '<a target="_blank" href="/show_similar_songs/' + a.filename + '">Link</a>';
      return [a.song_name, a.num_of_inst, a.num_of_simSongs, link_to_similarSongs];
    })
    if($('#songs_for_instrument_table_wrapper').length) {
      $('#songs_for_instrument_table').DataTable().clear().destroy();
    }
    $('#songs_for_instrument_table').DataTable( {
      data: data_song,
      columns: [  { title: "Song Name" },
                  { title: "Number of Instruments" },
                  { title: "Number of Similar Songs" },
                  { title: "Link to Similar Songs"} ],
      "order": [[ 1, "desc" ]],
      "language": {
          "lengthMenu": "Show _MENU_ songs",
          "zeroRecords": "No songs to show",
          "info": "Showing _START_ to _END_ of _TOTAL_ songs",
          "infoEmpty":      "No songs",
          "infoFiltered":   "(filtered from _MAX_ songs)"
      }
    });
  };
  $.ajax({
    type: "POST",
    url: '/get_songs_for_instruments',
    contentType: 'application/json',
    data: JSON.stringify(postObj),
    dataType: 'json',
    success: success
  });
}

function load_songList() {
  $.get("load_index", function(data, status){
    $('.ViolinSpan').html(makeUL(data['Violin']));
    $('.ClarinetSpan').html(makeUL(data['Clarinet']));
  });
}

function makeUL(array) {
    var list = document.createElement('ul');
    for (var i = 0; i < array.length; i++) {
        var a = document.createElement('a');
        a.href = '/show_similar_songs/' + array[i][1];
        a.target = '_blank';
        var item = document.createElement('li');
        item.appendChild(document.createTextNode(array[i][0]));
        a.appendChild(item);
        list.appendChild(a);
    }
    return list;
}
