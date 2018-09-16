'use strict';

function pause() {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        chrome.tabs.executeScript(
            tabs[0].id,
            {code: 'document.getElementsByTagName("video")[0].pause();'});
    });
}

function play() {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        chrome.tabs.executeScript(
            tabs[0].id,
            {code: 'document.getElementsByTagName("video")[0].play();'});
    });
}

function goTo(time) {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        chrome.tabs.executeScript(
            tabs[0].id,
            {code: 'document.getElementsByTagName("video")[0].currentTime=' + time + ';'});
    });
}

function injectLibrary(url, callback) {

    // https://humanwhocodes.com/blog/2009/07/28/the-best-way-to-load-external-javascript/

    var code = 'var script = document.createElement("script")\n' +
               'script.type = "text/javascript";\n' +
               'script.src = "' + url + '";\n' +
               'document.getElementsByTagName("head")[0].appendChild(script); swal("hellooo");'

    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        chrome.tabs.executeScript(
            tabs[0].id,
            {code: code}, function() {
                callback();
            });
    });
}

chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        switch (request.command) {
            case "checkTab":
                chrome.pageAction.show(sender.tab.id);

                var config = {
                    apiKey: "AIzaSyCIRwF_GRv3mv5TJdk41lI0Cs75ous1JyM",
                    authDomain: "hack-216504.firebaseapp.com",
                    databaseURL: "https://hack-216504.firebaseio.com",
                    projectId: "hack-216504",
                    storageBucket: "hack-216504.appspot.com",
                    messagingSenderId: "449878405558"
                };

                firebase.initializeApp(config);

                firebase.firestore().settings({
                    timestampsInSnapshots: true
                });

                firebase.firestore().enablePersistence()
                    .then(function() {
                        return firebase.auth().signInAnonymously();
                    })
                    .then(function() {

                        alert('firebase shit is working')

                        /*
                        injectLibrary('https://cdnjs.cloudflare.com/ajax/libs/sweetalert/2.1.0/sweetalert.min.js', function() {
                        */
                        /*
                        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
                            chrome.tabs.executeScript(
                                tabs[0].id,
                                {code: 'swal("Hello, world!")'});
                        });*/

                        var url = sender.tab.url;

                        if (1) { // url known
                            // get shit pls
                        } else {
                            // add 2 queue

                            // start listener
                        }

                        /*
                        });*/

                    }).catch(function(err) {
                        alert(err);
                    });

                break;
            case 'hrrr':

                chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
                    chrome.tabs.executeScript(
                        tabs[0].id,
                        {code: 'swal("Hello, world!")'});
                });

                goTo(20);
                break;

        }

    });

chrome.runtime.onInstalled.addListener(function() {

    var config = {
        apiKey: "<API_KEY>",
        authDomain: "<PROJECT_ID>.firebaseapp.com",
        databaseURL: "https://<DATABASE_NAME>.firebaseio.com",
        projectId: "<PROJECT_ID>",
        storageBucket: "<BUCKET>.appspot.com",
        messagingSenderId: "<SENDER_ID>",
    };
    firebase.initializeApp(config);

});

/*
chrome.runtime.onInstalled.addListener(function() {
    chrome.declarativeContent.onPageChanged.removeRules(undefined, function() {
        chrome.declarativeContent.onPageChanged.addRules([{
            conditions: [new chrome.declarativeContent.PageStateMatcher({
                pageUrl: {hostEquals: 'www.youtube.com'},
            })],
            actions: [new chrome.declarativeContent.ShowPageAction()]
        }]);
    });
});*/