from flask import Flask,request
from MutualExclusion.original_algorithm import Node
import os
from threading import Lock

app = Flask(__name__)
node = None
lock = Lock()

@app.before_first_request
def setup_graph():
    node_id = int(os.getenv("node_id"))
    OG,IC = [],[]
    for i in range(10,0,-1):
        if i<node_id:
            IC.append(i)
        elif i>node_id:
            OG.append(i)
    global node #I am going to regret doing this
    status = "critical" if node_id == 0 else "remainder"
    hasToken = True if node_id == 0 else False
    node = Node(node_id = node_id,status = status,hasToken=hasToken,OG=OG,IC=IC)


@app.route('/request')
def start():
    global node
    node.Recv("Request")