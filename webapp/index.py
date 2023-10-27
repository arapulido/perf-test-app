from flask import Flask, request
import requests
import threading

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/do_request")
def do_work():

    nthreads_sync = int(request.args.get('nthreads_sync', 2))
    nthreads_async = int(request.args.get('nthreads_async', 2))
    cycles_sync = int(request.args.get('cycles_sync', 5000000))
    cycles_async = int(request.args.get('cycles_async', 5000000))
    call_type = request.args.get('type', 'both')

    payload = {'nthreads': nthreads_sync, 'cycles': cycles_sync}

    if call_type in ('both', 'sync'):
        requests.get('http://sync:5001/load', params=payload)

    print("Finished sync calls")

    payload = {'nthreads': nthreads_async, 'cycles': cycles_async}

    if type in ('both', 'async'):
        t = threading.Thread(target=async_call, args=(payload,))
        t.daemon = True
        t.start()

    return 'Finished calls!', 200
