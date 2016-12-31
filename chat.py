from flask import Flask, render_template, url_for
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'webble_wobble'
io = SocketIO(app)

# This snippet stops it from caching my css


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


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
    send_data = {'partner': user1, 'room': room}
    send_data2 = {'partner': user2, 'room': room}
    join_room(room)
    emit('chat_started', send_data, room=chat_id2)
    emit('set_partner', send_data2, broadcast=False, include_self=True)


@io.on('add_to_room')
def add_to_rom(room):
    join_room(room)
    print (room)
    emit('room_connect', room=room)


@io.on('close_box')
def remove_partner(partner):
    emit('remove_partner', partner)


@io.on('sent_message')
def sent_message(data):
    room = data['room']
    emit('receive_message', data, include_self=False, room=room)


if __name__ == '__main__':
    io.run(app)
