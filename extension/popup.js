$(document).ready(function() {
    $('#pause').on('click', function() {

        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            chrome.runtime.sendMessage({command: "pause"});
        });

    });
});
