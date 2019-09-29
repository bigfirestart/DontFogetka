$(document).ready(function() {
    var mutationObserver = new MutationObserver(function(records) {
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
            $('.save-flight-btn').remove();
            var $carrLinks = $('.ticket-desktop__carriers-link');

            console.log('need update!');
            var button = $('<img>');
            button.click(() => {
                    var info = getFlightInfoFromPage(button[0]);
                    console.log( JSON.stringify(info) );

                    var message = {
                        type: 'choose-flight',
                        flightInfo: info
                    };

                    chrome.runtime.sendMessage(message, function(response) {
                        console.log(response.message);
                    });
                })
                .attr('src', chrome.extension.getURL('resources/icon-light.svg'))
                .addClass('save-flight-btn')
                .insertAfter($carrLinks);
                
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

    var $ticketSegmentList = $listItem.find('.ticket-desktop__segment');
    var transitCount = $ticketSegmentList.length;

    var $ticketFirstSegment = $ticketSegmentList.first();
    var $ticketLastSegment;

    if (transitCount > 1) {
        $ticketLastSegment = $ticketSegmentList.last();

        info.return_date = $ticketLastSegment
            .find('.segment-route__endpoint.origin')
            .find('.segment-route__date')
            .text();
    }
    
    info.departure_point = $ticketFirstSegment
        .find('.segment-route__endpoint.origin')
        .find('.segment-route__city')
        .text();

    info.destination_point = $ticketFirstSegment
        .find('.segment-route__endpoint.destination')
        .find('.segment-route__city')
        .text();
    
    info.arrival_date = $ticketFirstSegment
        .find('.segment-route__endpoint.destination')
        .find('.segment-route__date')
        .text();

    return info;
}