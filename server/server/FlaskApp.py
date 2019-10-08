#!/usr/bin/env python
from flask import Flask, render_template
import sys
modpath = '/home/nico/catkin_ws/src/semantic_web/src'
sys.path.insert(0, modpath)
from flask_socketio import SocketIO
from uploader import ontology

app = Flask(__name__)
socketio = SocketIO(app)
KnowledgeBase = ontology()


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('refresh_data')
def load_data():
    data = KnowledgeBase.get_instances()
    if data:
        for i in data:
            socketio.emit("refresh_page", i, callback="Update Page")


@socketio.on('handle_instance')
def update_instance(msg):
    name = msg["name"]
    type = msg["type"]
    action = msg["action"]
    print ("{} instance name {} {}".format(action, name, type))
    new_msg = KnowledgeBase.handle_instance(name, type, action)
    if action == "delete":
        new_msg = "Instance deleted"
    socketio.emit('server_response', new_msg, callback="Message Received")


@socketio.on('handle_data')
def update_instance_data(msg):
    instance = msg["name"]
    property = msg["type"]
    value = msg["value"]
    print ("{} instance type {} {}".format(instance, property, value))
    res = KnowledgeBase.update_property(instance, property, value)
    socketio.emit('server_response', res, callback="Message Received")


@socketio.on('refresh_relationship')
def update_relationship():
    data = KnowledgeBase.get_relationship()
    if data:
        for i in data:
            socketio.emit("refresh_rel_list", i, callback="Update Page")


@socketio.on('handle_relationship')
def handle_relationship(msg):
    data = []
    if len(msg) > 1:
        data = msg["relates"]
        name1 = msg["name1"]
        name2 = msg["name2"]
        res = KnowledgeBase.handle_relationship(data, name1, name2)
    else:
        data = msg["relates"]
        res = KnowledgeBase.handle_relationship(data)
    if data:
        socketio.emit('server_response', res, callback="Message Received")


if __name__ == '__main__':
    # socketio.run(app, host="192.168.100.16")
    socketio.run(app, host="localhost")
