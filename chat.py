from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'webble_wobble'
io = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@io.on('my_event')
def event_handler(json):
    print('Event: '+str(json))


@io.on('message')
def message_handler(msg):
    print('Message: ' + msg)
    send(msg, broadcast=True)


if __name__ == '__main__':
    io.run(app)
