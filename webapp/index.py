from flask import Flask
import requests
import threading

app = Flask(__name__)

def async_call():
    requests.get('http://async:5002/load?nthreads=2&cycles=10000000')

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/do_request")
def do_work():

    requests.get('http://sync:5001/load?nthreads=2&cycles=10000000')

    print("Finished sync calls")

    t = threading.Thread(target=async_call)
    t.daemon = True
    t.start()

    return 'Finished calls!', 200