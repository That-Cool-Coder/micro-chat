import socketio
import eventlet

port = 5000
sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={})

@sio.event
def connect(sid, environ):
    print('Connect')

def run():
    eventlet.wsgi.server(eventlet.listen('', port), app)

run()