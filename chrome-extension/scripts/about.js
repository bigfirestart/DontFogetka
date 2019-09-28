$(document).ready(function() {
    renderSavedFlights();
});

function renderSavedFlights() {
    chrome.storage.sync.get('flights', res => {
        var infoArr = res.flights.arr;
        if (!infoArr) return;
        
        var $flightsList = $('#flights-list');

        for(var i = 0; i < infoArr.length; ++i) {
            var $item = $('<div>').text('From: ' + infoArr[i].departure_point);
            $flightsList.append($item);
        }
    });
}

