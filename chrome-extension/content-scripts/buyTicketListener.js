document.addEventListener('click', function(event) {
    console.log('Click target: ' + event.target);

    var currElem = event.target;
    while(true) {        
        if (!currElem.classList || !currElem.classList.contains('buy-button')) {
            if (currElem.parentNode) 
                currElem = currElem.parentNode;
            else return;
        } else break;
    }

    console.log('You\'ve clicked buy button');
    chrome.runtime.sendMessage({ message: 'You\'ve clicked buy button' }, function(response) {
        console.log(response.message);
    });
});