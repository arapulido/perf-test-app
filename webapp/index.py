from flask import Flask, request
import requests
import threading
from ddtrace import tracer

app = Flask(__name__)

def async_call(payload, trace_ctx=None):
    tracer.context_provider.activate(trace_ctx)
    with tracer.trace("async_call"):
        requests.get('http://async:5002/load', params=payload)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route("/do_work")
def do_work():

    ncpus_sync = int(request.args.get('ncpus_sync', 2))
    ncpus_async = int(request.args.get('ncpus_async', 2))
    timeout_sync = int(request.args.get('timeout_sync', 60))
    timeout_async = int(request.args.get('timeout_async', 60))
    load_sync = int(request.args.get('load_sync', 100))
    load_async = int(request.args.get('load_async', 100))

    call_type = request.args.get('type', 'both')

    payload = {'ncpus': ncpus_sync, 'load': load_sync, 'timeout': timeout_sync}

    if call_type in ('both', 'sync'):
        with tracer.trace("sync_call"):
            requests.get('http://sync:5001/load', params=payload)

    print("Finished sync calls")

    payload = {'ncpus': ncpus_async, 'load': load_async, 'timeout': timeout_async}

    if call_type in ('both', 'async'):
        t = threading.Thread(target=async_call, args=(payload, tracer.current_trace_context(), ))
        t.daemon = True
        t.start()

    return 'Finished calls!', 200
