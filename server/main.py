from flask import Flask, request, Response
import multiprocessing
import firebase_admin
from firebase_admin import credentials, firestore
from videoProcessing import video

app = Flask(__name__)

cred = credentials.Certificate("servicekey.json")
firebase_admin.initialize_app(cred)

@app.route('/api/process', methods=['POST'])
def process():
    data = request.get_json()

    response = Response()

    print('Incoming request...', data)

    seizureCoefficient = video('https://www.youtube.com/watch?v=' + data['url']).scores
    #seizureCoefficient = [1,2,3]

    firebase_admin.firestore.client(app=None).collection('videos').document(data['url']).set({'coefficient':seizureCoefficient})
    firebase_admin.firestore.client(app=None).collection('queue').document(data['url']).delete()

    return 'ok'

if __name__ == '__main__':
    app.run()

#print(video('https://www.youtube.com/watch?v=Wu-KAY3lJ6A').scores)

