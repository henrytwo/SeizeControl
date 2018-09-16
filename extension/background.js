'use strict';

var isSetup = false;
var bs = [52, 25, 78, 80, 37, 80, 96, 4, 76, 13, 58, 96, 54, 22, 86, 16, 27, 0, 99, 49, 9, 92, 41, 65, 57, 68, 55, 24, 23, 9, 28, 29, 61, 98, 90, 34, 10, 14, 10, 44, 23, 64, 63, 61, 59, 50, 48, 59, 2, 86, 6, 3, 21, 36, 58, 28, 99, 81, 9, 98, 14, 61, 70, 28, 74, 73, 94, 77, 97, 92, 26, 81, 81, 61, 2, 49, 27, 51, 65, 39, 6, 94, 70, 27, 85, 68, 72, 70, 76, 77, 25, 8, 37, 19, 12, 28, 12, 14, 7, 26];
var threshhold = 10;

/**
 * Get YouTube ID from various YouTube URL
 * @author: takien
 * @url: http://takien.com
 * For PHP YouTube parser, go here http://takien.com/864
 */

function YouTubeGetID(url){
    var ID = '';
    url = url.replace(/(>|<)/gi,'').split(/(vi\/|v=|\/v\/|youtu\.be\/|\/embed\/)/);
    if(url[2] !== undefined) {
        ID = url[2].split(/[^0-9a-z_\-]/i);
        ID = ID[0];
    }
    else {
        ID = url;
    }
    return ID;
}

function listen(id) {
    var db = firebase.firestore();

    //alert("ok we listening")
    var listener = db.collection("videos").doc(id).onSnapshot(function(data) {
        if (data.exists) {

            sessionStorage.setItem(YouTubeGetID(url), JSON.stringify(data.get('coefficient')));

            alert('Video processed!')
            listener(); // Terminate
        }
    })

}

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

function getTime() {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        chrome.tabs.executeScript(
            tabs[0].id,
            {code: 'document.getElementsByTagName("video");'}, function (videoElement) {

                // Some dark magic going on here
                try {
                    if (videoElement[0] !== undefined) {
                        chrome.tabs.query({active: true, currentWindow: true}, function (tabs) {
                            chrome.tabs.executeScript(
                                tabs[0].id,
                                {code: 'document.getElementsByTagName("video")[0].currentTime;'}, function (videoTime) {

                                    //alert(JSON.stringify(sessionStorage));
                                    var seizureCoefficient = JSON.parse(sessionStorage.getItem(YouTubeGetID(tabs[0].url)));

                                    if (!!seizureCoefficient) {

                                        var timestamp = Math.round(videoTime);

                                        if (timestamp < seizureCoefficient.length) { // is dis thing in range?

                                            if (seizureCoefficient[timestamp] >= threshhold) { // is dis thing cause problemo>
                                                for (var i = timestamp; i < seizureCoefficient.length; i++) {
                                                    if (seizureCoefficient[i] < threshhold) {
                                                        goTo(i);

                                                        break;
                                                    }
                                                }
                                            }

                                        }
                                    }
                                });
                        });
                    }
                } catch (e) {
                    //alert(e);
                }
            })
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

                setup();

                chrome.pageAction.show(sender.tab.id);

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

                if (url != YouTubeGetID(url)) {

                    //alert(YouTubeGetID(url));

                    //sessionStorage.seizureCoefficient[YouTubeGetID(url)] = 'asdasdasd';

                    //sessionStorage.setItem(YouTubeGetID(url), JSON.stringify(bs));

                    var db = firebase.firestore();

                    db.collection("videos").doc(YouTubeGetID(url))
                        .get()
                        .then(function (doc) {

                            if (doc.exists) { // url known
                                //alert('lmao i fcking know what this is')
                                //console.log(doc.data());

                                sessionStorage.setItem(YouTubeGetID(url), JSON.stringify(doc.get('coefficient')));

                                // get shit pls
                            } else {

                                db.collection("queue").doc(YouTubeGetID(url))
                                    .get()
                                    .then(function (doc) {

                                        if (doc.exists) {

                                            alert('Video is being processed')
                                            listen(YouTubeGetID(url));

                                        } else {

                                            var db = firebase.firestore();

                                            alert('This is a new video. Please wait a moment as we process this request.')
                                            db.collection("queue").doc(YouTubeGetID(url))
                                                .set({})
                                                .then(function(docRef) {
                                                    listen(YouTubeGetID(url));
                                                })
                                                .catch(function(error) {
                                                    alert(error)
                                                    //console.error("Error adding document: ", error);
                                                });

                                        }
                                    });

                                // add 2 queue

                                // start listener
                            }

                        })
                        .catch(function (error) {
                            alert(error)
                        });

                    /*
                    });*/
                }

                break;

                /*
            case 'hrrr':

                chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
                    chrome.tabs.executeScript(
                        tabs[0].id,
                        {code: 'swal("Hello, world!")'});
                });

                goTo(20);
                break;*/

        }

    });

chrome.runtime.onInstalled.addListener(function() {
    setup();
});

function setup() {
    if (!isSetup) {
        isSetup = true;

        //sessionStorage.seizureCoefficient = {};

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

        firebase.auth().signInAnonymously();

        setInterval(getTime, 1000);
    }
}

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