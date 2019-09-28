chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        if (!request.type || !request.type === 'choose-flight') return;
        console.log('Notification: user have chosen flight');

        saveFlightInfo(request.flightInfo);

        var addedListener = () => {
            sendResponse({
                message: 'done',    
            });
        };
        
        showFlightAddedNotification(addedListener, removeLastFlight);
    });

function showFlightAddedNotification(addedListener, removeCallback) {
    var iconUrl = './resources/icon-night.svg';
    console.log(iconUrl);

    var notifOpt = {
        type: 'basic',
        title: 'Nezabudka',
        message: 'You can setup the travel list for this flight by clicking to the extension\'s button',
        iconUrl: iconUrl,

        buttons: [
            {
                title: 'Got it!'
            },
            {
                title: 'Remove'
            }
        ]
    };

    chrome.notifications.clear('notif', () => {
        chrome.notifications.create('notif', notifOpt, function(id) {
            chrome.notifications.onButtonClicked.addListener((id, btnIndex) => {
                if (id === 'notif' && btnIndex === 1) {
                    removeCallback();
                }

                chrome.notifications.clear(id);
            });

            chrome.notifications.onClosed(id => {
                chrome.notifications.clear(id);
            });

            addedListener();
        });
    });
}

function saveFlightInfo(info) {
    chrome.storage.sync.get('flights', res => {
        console.log('flights are: ' + JSON.stringify(res.flights));

        var infoArr;
        if (!res.flights || !res.flights.arr) infoArr = [info];
        else {
            infoArr = res.flights.arr;
            infoArr.push(info);
        }

        console.log('Info arr is: ' + JSON.stringify(infoArr));

        chrome.storage.sync.set({ 
            flights: {
                arr: infoArr
            } 
        });
    });
}

function removeLastFlight() {
    chrome.storage.sync.get('flights', res => {

        if (!res.flights || !res.flights.arr || !res.flights.arr.length === 0)
            return;

        var infoArr = res.flights.arr;
        infoArr.pop();

        chrome.storage.sync.set({ 
            flights: {
                arr: infoArr
            }
        });
    });
}

