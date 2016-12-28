from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit, join_room, leave_room
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
    emit('new_user', user, broadcast=True)


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


@io.on('start_chat')
def chat_start(data):
    user1 = data['person1']
    user2 = data['person2']
    chat_id2 = data['chatId2']
    room = user1+user2
    join_room(room)
    emit('chat_started', room, room=chat_id2)


@io.on('add_to_room')
def add_to_rom(room):
    join_room(room)
    emit('room_connect', room, room=room)


if __name__ == '__main__':
    io.run(app)
