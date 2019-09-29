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
                .click(ev => {
                    chrome.storage.sync.get('flights', res => {
                        if (!res.flights || !res.flights.arr) return;

                        var flight = res.flights.arr[i];

                        var goToPage = () => {
                            chrome.tabs.create({
                                active: true,
                                url: 'travelEdit.html'
                            });
                        };

                        chrome.storage.sync.set({ 'active-flight': flight }, goToPage);
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
                .text('x')
                .addClass('remove-btn')
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
