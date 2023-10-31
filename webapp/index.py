from flask import Flask, request
import requests
import threading

app = Flask(__name__)

def async_call(payload):
    requests.get('http://async:5002/load', params=payload)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/do_request")
def do_work():

    nthreads_sync = int(request.args.get('nthreads_sync', 2))
    nthreads_async = int(request.args.get('nthreads_async', 2))
    timeout_sync = int(request.args.get('timeout_sync', 60))
    timeout_async = int(request.args.get('timeout_async', 60))
    call_type = request.args.get('type', 'both')

    payload = {'nthreads': nthreads_sync, 'timeout': timeout_sync}

    if call_type in ('both', 'sync'):
        requests.get('http://sync:5001/load', params=payload)

    print("Finished sync calls")

    payload = {'nthreads': nthreads_async, 'timeout': timeout_async}

    if call_type in ('both', 'async'):
        t = threading.Thread(target=async_call, args=(payload,))
        t.daemon = True
        t.start()

    return 'Finished calls!', 200
