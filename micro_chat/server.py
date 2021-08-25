import socketio
import eventlet

from .message import Message

class Server:
    def __init__(self):
        self.password = input('Enter a password for the server ' + 
            '(type nothing for free access) ')
        if self.password == '':
            self.password = None

        self.port = 5000

        self.sio = socketio.Server()

        # create app so that eventlet has something to run
        # there's probably a better way but I can't find it
        self.app = socketio.WSGIApp(self.sio, static_files={
            '/': f'/frontend/'
        })

        self.messages = []
        @self.sio.event
        def connect(sid, environ, auth: str):
            '''
            Expects auth to be str containing password
            '''
            if self.password is not None and \
                auth['password'] != self.password:
                self.sio.disconnect(sid)

        @self.sio.event
        def send(sid, sender_name, content):
            self.messages.append(Message(sender_name, content))

    def run(self):
        eventlet.wsgi.server(eventlet.listen(('', self.port)), self.app)