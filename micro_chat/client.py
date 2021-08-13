import socketio

class Client:
    def __init__(self):

        self.client = socketio.Client()
        
        @self.client.on('connect')
        def connect():
            print('Connected')

        @self.client.on('disconnect')
        def disconnect():
            print('Disconnected')

    def run(self):
        self.server_address = input('Enter address of server: ')
        self.password = 'sus'
        self.client.connect(self.server_address, auth=self.password)