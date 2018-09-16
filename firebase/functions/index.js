const functions = require('firebase-functions');
const request = require('request');

// // Create and Deploy Your First Cloud Functions
// // https://firebase.google.com/docs/functions/write-firebase-functions
//

/*
exports.helloWorld = functions.https.onRequest((request, response) => {
    response.send("Hello from Firebase!");
});*/

exports.dequeueVideo = functions.firestore
    .document('queue/{videoId}')
    .onCreate(function(snap, context) {
        // Get an object representing the document
        // e.g. {'name': 'Marie', 'age': 66}
        const newValue = snap.data();

        console.log(snap, context.params.videoId)

        // access a particular field as you would any JS property
        const name = newValue.name;

        var url = context.params.videoId;

        console.log(url);

        /*
        request('https://htn.henrytu.me', function (error, response, body) {
            if (!error && response.statusCode == 200) {
                return Promise.resolve('ok');
            }
        });*/

        request.post({
            url: 'https://htn.henrytu.me/api/process',
            json: {
                url: url
            },
            headers: {
                'Content-Type': 'application/json'
            },
        }, function(e, r, b) {
            if (!e && r.statusCode == 200) {
                return Promise.resolve('ok');
            }
        })

        // perform desired operations ...
    });
