// We first create a 'map' and 'coord' variable
var map;
var coord = {};

// Function calling the google map object
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
  
  // We define a special marker for our map
  var marker = new google.maps.Marker({
    position: coord,
    map: map,
    animation: google.maps.Animation.DROP,
    title: "C'est ici mon petit!"
  });
}

/* When the user submit a request, it is caught by this function.
 A loader appears while processing the request and then the function
 prints the result to the web page */
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

