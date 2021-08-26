import socketio
import eventlet

class Server:
    def __init__(self):
        self.password = input('Enter a password for the server: ')

        self.port = 5000

        self.sio = socketio.Server()

        # Dict of {sessionId : username}
        self.client_usernames = {}

        # create app so that eventlet has something to run
        # there's probably a better way but I can't find it
        self.app = socketio.WSGIApp(self.sio)

        @self.sio.on('connect')
        def connect(sid, environ, auth: dict):
            '''
            Expects auth to be like so:
            {username : 'some string', password: 'some string'}
            '''
            if auth['password'] != self.password:
                username = auth['username'] # can't use dict access in f-string
                print(f'Rejected connection from "{username}" - password incorrect')
                self.sio.disconnect(sid)
            elif auth['username'] in self.client_usernames.values():
                username = auth['username'] # can't use dict access in f-string
                print(f'Rejected connection from "{username}"" - username already used')
                self.sio.disconnect(sid)
            else:
                username = auth['username'] # can't use dict access in f-string
                print(f'Accepted connection from "{username}"')
                self.client_usernames[sid] = username
        
        @self.sio.on('disconnect')
        def disconnect(sid):
            username = self.client_usernames.get(sid, '<unknown>')
            print(f'Disconnected "{username}"')

        @self.sio.on('send')
        def send(sid, data):
            ''' Expects data to be like so:
            {sender : 'some string' (must correspond to username in username table),
                content : 'some string'}
            '''
            
            if 'sender' not in data or 'content' not in data:
                return

            self.sio.emit('message', data)

    def run(self):
        eventlet.wsgi.server(eventlet.listen(('', self.port)), self.app)