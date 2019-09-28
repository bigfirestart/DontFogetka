$(document).ready(function() {
    renderSavedFlights();
});

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

        for(var i = 0; i < infoArr.length; ++i) {
            
            /* 
            var $item = $('<div>')
                .addClass('flight-item');

            var $depart = $('<div>')
                .addClass('') */

            var $item = $('<div>')
                .addClass('flight-item')
                .text(infoArr[i].departure_point + '=>' + infoArr[i].destination_point);

            var $setupRef = $('<a>')
                .attr('href', '#')
                .text('set up')
                .click(ev => {
                    chrome.tabs.create({
                        active: true,
                        url: 'travelEdit.html'
                    });
                })
                .appendTo($item);

            var $removeBtn = $('<button>')
                .click(ev => {
                    var $target = $(ev.originalEvent.target).parent();
                    var index = $flightsList.children().index($target);
                    removeFlight(index, () => {
                        renderSavedFlights();
                    });
                })
                .text('remove')
                .appendTo($item);

            $flightsList.append($item);
        }
    });
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
