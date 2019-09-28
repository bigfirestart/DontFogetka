document.addEventListener('click', function(event) {

    var button = closestByClassName(event.target, 'buy-button');
    if (!button) return;

    console.log('User have clicked buy button');

    var info = getFlightInfoFromPage(button);
    console.log( JSON.stringify(info) );

    var message = {
        type: 'choose-flight',
        flightInfo: info
    };

    chrome.runtime.sendMessage(message, function(response) {
        console.log(response.message);
    });
});

function closestByClassName(elem, className) {
    var currElem = elem;

    while(true) {        
        if (!currElem.classList || !currElem.classList.contains(className)) {
            if (currElem.parentNode) 
                currElem = currElem.parentNode;
            else return;
        } else {
            return currElem;
        };
    }
}

    /*
    {
        "departure_point" : "Moscow",
        "destination_point" : "London",
        "arrival_date" : "23.09.2019",
        "return_date" : "01.10.2019",
        "travel_type" : ["beach", "run" , "safari"],
        "people" : {
            "count": 3,
            "tourists" : [
                {
                    "gender": "male",
                    "adult": true
                },
                {
                    "gender": "female",
                    "adult": true
                },
                {
                    "gender": "male",
                    "adult": false
                }
            ]
        }
    }
    */

function getFlightInfoFromPage(buttonElem) {
    var info = {};

    var listItem = closestByClassName(buttonElem, 'product-list__item');
    var $listItem = $(listItem);

    var $ticketFirstSegment = $listItem.find('.ticket-desktop__segment:first-child');
    var $ticketLastSegment = $listItem.find('.ticket-desktop__segment:last-child');
    
    info.departure_point = $ticketFirstSegment
        .find('.segment-route__endpoint.origin')
        .find('.segment-route__city');

    info.departure_point = info.departure_point.text();

    info.destination_point = $ticketFirstSegment
        .find('.segment-route__endpoint.destination')
        .find('.segment-route__city')
        .text();
    
    info.arrival_date = $ticketFirstSegment
        .find('.segment-route__endpoint.destination')
        .find('.segment-route__date')
        .text();

    info.return_date = $ticketLastSegment
        .find('.segment-route__endpoint.origin')
        .find('.segment-route__date')
        .text();

    return info;
}