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
        $('.loader').hide();
      }
    });
    $('.hidden').show();
  }
);

