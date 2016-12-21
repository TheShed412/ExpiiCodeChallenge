from flask import Flask
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'webble_wobble'
io = SocketIO(app)

if __name__ == '__main__':
    io.run(app)
