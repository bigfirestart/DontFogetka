chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        if (!request.type || !request.type === 'choose-flight') return;
        console.log('Notification: user have chosen flight');

        var doneListener = () => {
            sendResponse({
                message: 'done',    
            });
        };

        var addCallback = () => {
            saveFlightInfo(request.flightInfo);
        };
        
        showFlightAddedNotification(doneListener, addCallback);
    });

function showFlightAddedNotification(doneListener, addCallback) {
    var iconUrl = './resources/icon-night.svg';
    console.log(iconUrl);

    var notifOpt = {
        type: 'basic',
        title: 'Nezabudka',
        message: 'Вы желаете запомнить этот вариант перелета для дальнейшего планирования поездки?',
        iconUrl: iconUrl,

        buttons: [
            {
                title: 'Да'
            },
            {
                title: 'Нет'
            }
        ]
    };

    chrome.notifications.clear('notif', () => {
        chrome.notifications.create('notif', notifOpt, function(id) {
            chrome.notifications.onButtonClicked.addListener((id, btnIndex) => {
                if (id === 'notif' && btnIndex === 0) {
                    addCallback();
                }

                chrome.notifications.clear(id);
            });

            chrome.notifications.onClosed.addListener(id => {
                chrome.notifications.clear(id);
            });

            doneListener();
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
