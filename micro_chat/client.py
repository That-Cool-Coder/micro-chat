import sys
import string

import socketio
import readchar

class Client:
    CTRL_C = '\x03'
    CTRL_Z = '\x1a'
    BACKSPACE_CHAR = '\x7f'
    NEWLINE_CHAR_CODE = 13
    PRINTABLE_CHARS = list(string.ascii_letters + string.digits + string.punctuation + ' ')

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
        
        @self.client.on('message')
        def message(data):
            sender = data['sender']
            content = data['content']
            if sender != self.username:
                self.print_output(f'[{sender}] {content}')
        
        @self.client.on('connect_error')
        def connect_error(data):
            print('Connection failed due to susu')

        @self.client.on('disconnect')
        def disconnect():
            self.print_output('Disconnected')

    def run(self):
        self.server_address = 'http://' + input('Enter address of server (eg 1.2.3.4:1234): ')
        self.server_password = input('Enter password of server: ')
        self.username = input('Enter username to use: ')
        try:
            self.client.connect(self.server_address,
                auth={'username' : self.username, 'password' : self.server_password})
            self.input_loop()
        except (socketio.exceptions.ConnectionError,
            socketio.exceptions.ConnectionRefusedError):
            print('Failed to connect')
    
    def print_output(self, message):
        ''' Print output to the console, without messing up the input too much '''

        # Remove all invalid chars, to stop people from putting color escape codes, etc
        char_list = [char for char in list(message) if char in self.PRINTABLE_CHARS]
        cleaned_message = ''.join(char_list)

        if self.waiting_for_input:
            print('\r' + cleaned_message + '\r', flush=True)
            print('> ' + self.input_buffer, end='', flush=True)
        else:
            print(cleaned_message)
    
    def get_message(self):
        ''' Get a message from the user.
        Returns None if the user pressed KeyboardInterrupt'''

        self.input_buffer = ''
        self.waiting_for_input = True
        keyboard_interrupt_triggered = False
        print('> ', end='', flush=True)
        
        while self.waiting_for_input:
            char = readchar.readchar()
            print(char, end='', flush=True)

            # readchar blocks KeyboardInterrupt by default, so manually make it
            if char == self.CTRL_C  or char == self.CTRL_Z:
                self.client.disconnect()
                self.waiting_for_input = False
                keyboard_interrupt_triggered = True
                break
            # Send message on enter
            elif char == chr(self.NEWLINE_CHAR_CODE):
                self.waiting_for_input = False
            # Delete char on backspace
            elif char == '\b' or char == self.BACKSPACE_CHAR:
                if len(self.input_buffer) > 0:
                    sys.stdout.write('\b \b') # move left, clear char, move left
                    sys.stdout.flush()
                    self.input_buffer = self.input_buffer[:-1]
            # Normal behaviour
            elif char in self.PRINTABLE_CHARS:
                self.input_buffer += char
            # Make a bell noise on invalid chars
            else:
                sys.stdout.write('\a')
                
        # Add newline to make next message not go on same line
        print('')

        if keyboard_interrupt_triggered:
            return None
        else:
            return self.input_buffer

    def input_loop(self):
        print('Enter a message: ')
        while True:
            message_content = self.get_message()
            if message_content is None:
                break

            self.client.emit('send',
                {'sender' : self.username, 'content' : message_content})