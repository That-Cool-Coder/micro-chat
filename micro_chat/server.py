from eventlet.green import socket
import socketio
import eventlet

class Server:
    port: int
    password: str
    sio: socketio.Server
    app: socketio.WSGIApp
    client_usernames: dict
    init_success: bool = False

    def __init__(self):
        port = input('Enter a port to run the server on: ')
        if not self.port_is_valid(port):
            print('Invalid port number')
            return
        self.port = int(port)

        self.password = input('Enter a password for the server: ')

        self.sio = socketio.Server()
        self.sio.quiet = True

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
                print(f'Rejected connection from "{username}" - username already used')
                self.sio.disconnect(sid)
            else:
                # Nominal case of success
                username = auth['username'] # can't use dict access in f-string
                print(f'Accepted connection from "{username}"')
                self.client_usernames[sid] = username
                self.sio.emit('user_joined', {'username' : username})
        
        @self.sio.on('disconnect')
        def disconnect(sid):
            username = self.client_usernames.get(sid, '<unknown>')
            print(f'Lost connection from "{username}"')

            if sid in self.client_usernames:
                del self.client_usernames[sid]
                self.sio.emit('user_left', {'username' : username})

        @self.sio.on('send')
        def send(sid, data):
            ''' Expects data to be like so:
            {sender : 'some string' (must correspond to username in username table),
                content : 'some string'}
            '''
            
            if 'sender' not in data or 'content' not in data:
                return

            self.sio.emit('new_message', data)
        
        self.init_success = True

    def port_is_valid(self, port: str):
        try:
            port_num = int(port)
            return 1 < port_num < 2 ** 16
        except:
            return False

    def run(self):
        if self.init_success:
            print('Running')
            try:
                eventlet.wsgi.server(eventlet.listen(('', self.port)), self.app, log_output=False)
            except PermissionError:
                print('Failed to run server: the port is already in use')
            except:
                print('Failed to run server')