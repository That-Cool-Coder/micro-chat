import socketio

class Client:
    def __init__(self):

        self.client = socketio.Client()
        
        @self.client.on('connect')
        def connect():
            print('\nConnected')
        
        @self.client.on('message')
        def message(data):
            sender = data['sender']
            content = data['content']
            print(f'\n [{sender}] {content}')

        @self.client.on('disconnect')
        def disconnect():
            print('\nDisconnected')

    def run(self):
        self.server_address = 'http://' + input('Enter address of server (eg 1.2.3.4:1234): ')
        self.password = input('Enter password of server: ')
        self.username = input('Enter username to use: ')
        try:
            self.client.connect(self.server_address,
                auth={'username' : self.username, 'password' : self.password})
            self.input_loop()
        except:
            print('Failed to connect')

    def input_loop(self):
        print('Enter a message: ')
        while True:
            message_content = input('>')
            self.client.emit('send',
                {'sender' : self.username, 'content' : message_content})