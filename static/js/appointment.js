let selectedDate = $('#selectedDate')

let appointmentButton = '<input type="submit" value="Отправить" id="appointmentButton">'
let doctor = $('#doctor').text()

function appendButton(data, button) {
    let slicedForm = data.slice(0, 785)
    slicedForm += button + '</form>'
    let addPostSlicedForm = slicedForm.slice(30)
    let formStart = "<form method='POST'>"
    formStart += addPostSlicedForm
    return formStart
}

jQuery.ajax({
    url: 'http://localhost:8000/appointment',
    type: 'get',
    success: function(data){
      $('#timeslotForm').append(appendButton(data, appointmentButton));
    },
    error: function () {
        $('#timeslotForm').append('<h5>Ошибка сервера</h5>');
    }

})

function AppointmentPost(date, doctor) {
    jQuery.ajax({
        url: 'http://localhost:8000/appointment',
        type: 'post',
        data: {
            'doctor': doctor,
            'date': date,
        },
        success: function(msg){
          alert( "Статус запроса: " + msg );
        },
        error: function(){
          alert( "Ошибка");
        },
    })
}

$('.calendar').datepicker({
        onSelect: function (dateText, inst) {
          if (selectedDate.text().length < 5) {
            selectedDate.append(dateText.slice(0,2))
          }
        }
});

$('#showAppointment').one('click', function(event) {
  $('#appointment').hide("fast");
})

$('#appointmentButton').one('click', function(event) {
    AppointmentPost(selectedDate.text(), doctor)
})