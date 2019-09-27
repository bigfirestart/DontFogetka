chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        console.log('Notification: user bought tickets');

        var iconUrl = './resources/icon.svg';
        console.log(iconUrl);

        var notifOpt = {
            type: 'basic',
            title: 'Nezabudka',
            message: 'You can setup the travel list for this flight by clicking to the extension\'s button',
            iconUrl: iconUrl
        };

        chrome.notifications.clear('notif');

        chrome.notifications.create('notif', notifOpt, function(id) {
        });

        sendResponse({
            message: 'done',    
        });
    });