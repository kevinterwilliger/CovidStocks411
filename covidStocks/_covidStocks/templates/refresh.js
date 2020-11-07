$('#clickme').click(function(evt){
    evt.preventDefault();
    $.ajax({
        synch: 'true',
        type: 'GET',
        url: '{% url 'name' %}',
        success: function(data){
            $('#content').html(data);
        }
    });
}
