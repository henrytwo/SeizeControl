const functions = require('firebase-functions');

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

        // access a particular field as you would any JS property
        const name = newValue.name;

        var url = 'https://www.youtube.com/watch?v=' + newValue.videoId;

        // perform desired operations ...
    });
