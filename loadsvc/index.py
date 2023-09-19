import time
import math
import sys
from multiprocessing import cpu_count, Process

from flask import Flask, request
app = Flask(__name__)

def generate_cpu_load(cycles):
    for i in range(0,cycles):
        math.sqrt(64*64*64*64*64)

@app.route("/")
def hello():
    output = "Number of cores: %d" % cpu_count()
    return output

@app.route("/load")
def do_work():
    nthreads = int(request.args.get('nthreads'))
    cycles = int(request.args.get('cycles'))

    processes = []
    for _ in range (nthreads):
        p = Process(target=generate_cpu_load, args=(cycles,))
        p.start()
        processes.append(p)
    for process in processes:
        process.join()

    return '', 200