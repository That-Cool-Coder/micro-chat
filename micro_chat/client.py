import socketio
import readchar

class Client:
    CONNECTION_REFUSED_BY_SERVER = 'Connection refused by the server'

    client: socketio.Client
    server_address: str
    server_password: str
    username: str
    waiting_for_input: bool = False
    input_buffer: str = ''

    def __init__(self):
        self.client = socketio.Client()
        
        @self.client.on('connect')
        def connect():
            self.print_output('Connected')
        
        @self.client.on('new_message')
        def message(data):
            sender = data['sender']
            content = data['content']
            if sender != self.username:
                self.print_output(f'[{sender}] {content}')
        
        @self.client.on('connect_error')
        def connect_error(data):
            if data == self.CONNECTION_REFUSED_BY_SERVER:
                print('Could not find server')
            else:
                print(data)

        @self.client.on('disconnect')
        def disconnect():
            self.print_output('Disconnected')

    def run(self):
        self.server_address = 'http://' + input('Enter address of server (eg 10.20.30.40:1234): ')
        self.server_password = input('Enter password of server: ')
        self.username = input('Enter username to use: ')
        try:
            self.client.connect(self.server_address,
                auth={'username' : self.username, 'password' : self.server_password})
            self.input_loop()
            self.client.wait()
        except (socketio.exceptions.ConnectionError,
            socketio.exceptions.ConnectionRefusedError):
            print('Failed to connect')
    
    def print_output(self, message):
        ''' Print output to the console without messing up the input too much '''

        if self.waiting_for_input:
            print('\r' + message + '\r', flush=True)
            print('> ', end='', flush=True)
        else:
            print(message)
    
    def get_message(self):
        ''' Get a message from the user.
        Returns None if the user pressed KeyboardInterrupt'''

        self.waiting_for_input = True
        print('', end='', flush=True) # flush using print because input doesn't allow flush=True
        message = input('> ')
        self.waiting_for_input = False
        return message

    def input_loop(self):
        print('Enter a message: ')
        while True:
            message_content = self.get_message()
            if message_content is None:
                break

            self.client.emit('send',
                {'sender' : self.username, 'content' : message_content})