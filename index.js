const functions = require("firebase-functions");
const admin = require('firebase-admin');
admin.initializeApp(functions.config().firebase);

token = 'dIMqDPjJS-2Mz4jW5BlJk1:APA91bG0HKyH_oNvf2P7hT16n0AmM0OpY-VVe3dbnyg-fsRwyE3f8orOWwHtWAVACs-qnPQuGO0EX66XRR57LDyHSxcQklOgHqhkhiaQ3rhLv-Nykqk2T_b3ISp8c7-yG31c4B2hTFxv'

exports.Notification = functions.database
    .ref('/{pushId}')
    .onCreate((snap, context) => {
        const newValue = snap.val();
        const name = newValue.name;

        var payload = {
            'notification': {
                'title': 'Visitor Detected',
                'body': name + ' just entered the home'
            }
        }

        var result = admin.messaging().sendToDevice(token, payload);
        return result;
});



