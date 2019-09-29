$(document).ready(function() {
    renderSavedFlights();
    $passProto = $('#pass-proto');
    $tripInfo = $('#trip-info');
    $passInfo = $('#pass-info');

    $('#cancel-btn').click(() => {
        gotoMainPage();
    });

    $('#done-btn').click(() => {
        sendTripInfo();
        gotoMainPage();
    });

    $('#add-pass-btn').click(addPassenger);
});

var $passProto;
var $tripInfo;
var $passInfo;

function gotoMainPage() {
    $('#saved-flights').removeClass('invisible');
    $('#trip-info,#pass-info,#done-btn,#cancel-btn').addClass('invisible');
    
    renderSavedFlights();
}

function gotoTripInfoPage(flight) {
    $('#saved-flights').addClass('invisible');
    $('#trip-info,#pass-info,#done-btn,#cancel-btn').removeClass('invisible');
    
    renderTripInfo(flight);
    renderPassInfo(flight);
}


function renderSavedFlights() {

    var $savedFlights = $('#saved-flights');
    var $flightsList = $savedFlights.children('#flights-list');
    var $noFlightsMsg = $savedFlights.children('#no-trips-msg');

    $savedFlights.children('*').removeClass('invisible');
    $flightsList.children().remove();

    chrome.storage.sync.get('flights', res => {
        if (!res.flights || !res.flights.arr)
            return;

        var infoArr = res.flights.arr;

        if (infoArr.length === 0) {
            $flightsList.addClass('invisible');
            return;
        }
        
        $noFlightsMsg.addClass('invisible');

        var createClickListener = function(i) {
            var _i = i;
            return () => gotoTripInfoPage(infoArr[_i]);
        }

        for(var i = 0; i < infoArr.length; ++i) {
            
            var $item = $('<div>')
                .addClass('flight-item both');

            var $depart = $('<div>')
                .text(infoArr[i].departure_point)
                .addClass('depart')
                .appendTo($item);

            var $destin = $('<div>')
                .text(infoArr[i].destination_point)
                .addClass('destin')
                .appendTo($item);

            var $date_to = $('<div>')
                .text(infoArr[i].arrival_date)
                .addClass('date-to')
                .appendTo($item);

            if (infoArr[i].return_date)
                var $date_from = $('<div>')
                    .text(infoArr[i].return_date)
                    .addClass('date-from')
                    .appendTo($item);

            var $setupRef = $('<button>')
                .text('set up')
                .click( createClickListener(i) )
                .appendTo($item);

            var $removeBtn = $('<button>')
                .click(ev => {
                    var $target = $(ev.originalEvent.target).parent();
                    var index = $flightsList.children().index($target);
                    removeFlight(index, () => {
                        renderSavedFlights();
                    });
                })
                .text('x')
                .addClass('remove-btn')
                .appendTo($item);

            $flightsList.append($item);
        }
    });
}

function renderTripInfo(flight) {
    $tripInfo.find('#depart-info').text(flight.departure_point);
    $tripInfo.find('#destin-info').text(flight.destination_point);
    $tripInfo.find('#date-to-info').text(flight.arrival_date);
    $tripInfo.find('#date-from-info').text(flight.return_date);
}

function renderPassInfo(flight) {

    $('#pass-container').children().remove();

    if (!flight.people || !flight.people.count) {
        addPassenger();
        return;
    }

    for (var i = 0; i < flight.people.count; ++i) {
        addPassenger();
    }
}

function removeFlight(index, refreshCallback) {
    chrome.storage.sync.get('flights', res => {
        var infoArr = res.flights.arr;
        if (!infoArr) return;

        infoArr = infoArr.filter((_, i) => i !== index);

        console.log( JSON.stringify(infoArr) );

        chrome.storage.sync.set({
            flights: {
                arr: infoArr
            }
        }, refreshCallback);
    });
}

function addPassenger() {
    var $person = $passProto.clone();
    $person
        .removeClass('invisible')
        .appendTo( $('#pass-container') );
}

function sendTripInfo() {
    var flight = {
        departure_point: $('#depart-info').text(),
        destination_point: $('#destin-info').text(),
        arrival_date: $('#date-to-info').text(),
        return_date: $('#date-from-info').text(),

        people: {
            tourits: []
        }
    };
    
    var $passangers = $('#pass-container');
    flight.people.count = $passangers.length;

    for (var i = 0; i < flight.people.count; ++i) {
        var $pass = $passangers.eq(i);
        flight.people.tourits.push({
            name: $pass.find('#name-id').val(),
            sex: $pass.find('radio[name=sex]:checked').val(),
            age: $pass.find('radio[name=age]:checked').val() === 'adult',
        });
    }

    console.log(JSON.stringify(flight));

    var uri = 'http://95.216.157.100:5000/';
    $.post(uri + 'build', JSON.stringify(flight))
    .done(res => {
        $.post(uri + 'save', JSON.stringify(res))
        .done(() => console.log('Visit trello'));
    });
}