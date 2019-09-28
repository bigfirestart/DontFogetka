$(document).ready(function() {
    var mutationObserver = new MutationObserver(function(records) {
        var $sideContent = $('.ticket-desktop__side-content');

        var needUpdate = false;
        records.forEach(record => {
            var list = record.addedNodes;
            for (var i = 0; i < list.length; ++i) {
                if ($(list[i]).find('.buy-button').length !== 0) {
                    needUpdate = true;
                    break;
                }
            }
        });

        if (needUpdate) {
            $('.nezabudka-btn').remove();

            console.log('need update!');
            var btn = $('<button>')
                .text('subscribe')
                .addClass('nezabudka-btn');

            var cont = $("<div>")
                .css('text-align', 'center')
                .appendTo($sideContent);
                
            btn.appendTo(cont);
        }
    });

    mutationObserver.observe(document, {
        subtree: true,
        childList: true
    });
});

document.addEventListener('click', function(event) {

    var button = closestByClassName(event.target, 'buy-button');
    if (!button)
        return;

    var $buttonSpan = $(button).children().find('.buy-button__text');
    if (!$buttonSpan)
        return;

    if ($buttonSpan.text() !== 'Купить') 
        return;

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