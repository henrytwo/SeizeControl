from flask import Flask, request, Response
import multiprocessing
import firebase_admin
from firebase_admin import credentials
from videoProcessing import video

app = Flask(__name__)

"""
cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
"""

@app.route('/api/process', methods=['POST'])
def process():
    data = request.get_json()

    response = Response()

    print(data)
    print(video(data['url']).scores)

    return 'ok'

if __name__ == '__main__':
    app.run()

#print(video('https://www.youtube.com/watch?v=Wu-KAY3lJ6A').scores)

