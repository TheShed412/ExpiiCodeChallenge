from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'webble_wobble'
io = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@io.on('my_event')
def event_handler(data):
    parse = json.loads(data)
    print('Event: '+parse['data'])


@io.on('add_user')
def add_user(user):
    io.emit('new_user', user)


@io.on('request_list')
def request_list():
    emit('send_list', broadcast=True, include_self=False)


@io.on('list_sent')
def send_list(users):
    io.emit('new_list', users, include_self=False)


@io.on('message')
def message_handler(msg):
    print('Message: ' + msg)
    send(msg, broadcast=True)


if __name__ == '__main__':
    io.run(app)
