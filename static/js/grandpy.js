var map;
var coord = {};
function initMap(coord) {
  map = new google.maps.Map(document.getElementById('map'), {
    center: coord,
    zoom: 15,
    styles: [
      {
        "featureType": "poi",
        "stylers": [
          { "visibility": "off" }
        ]
      }
    ]
  });
  var marker = new google.maps.Marker({
    position: coord,
    map: map,
    title: "C'est ici mon petit!"
  });
}


$('#questionform').submit (
  function (event) {
    event.preventDefault();
    var question = $('#question').val();
    $.ajax({
      url: '/ajax_search',
      type: 'POST',
      data: {question},
      dataType: 'json',
      success: function(data, statut){
        $('#result').text(data['answer']);
        $('#result').append(data['environment']);
        var coord = data['coord'];
        initMap(coord);
        $('.loader').hide();
      }
    });
    $('#hidden').show();
  }
);

