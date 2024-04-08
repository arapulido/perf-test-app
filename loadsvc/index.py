from multiprocessing import cpu_count
import subprocess

from flask import Flask, request
app = Flask(__name__)

@app.route("/")
def hello():
    output = "Number of cpus: %d" % cpu_count()
    return output

@app.route("/load")
def do_work():
    timeout = int(request.args.get('timeout', '60'))
    ncpus = int(request.args.get('ncpus', '2'))
    load = int(request.args.get('load', '100'))

    if load > 100:
        load = 100
    if load < 0:
        load = 0

    subprocess.run(["stress-ng", "--cpu", str(ncpus), "--cpu-load", str(load), "--cpu-load-slice", "100", "--timeout", str(timeout)])

    return '', 200
