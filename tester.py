import socketio
import eventlet

class Server:
    def __init__(self):

        self.port = 5000

        self.sio = socketio.Server()

        self.app = socketio.WSGIApp(self.sio, static_files={})

        @self.sio.event
        def connect(sid, environ):
            print('Connect')

    def run(self):
        eventlet.wsgi.server(eventlet.listen('', self.port), self.app)

Server().run()