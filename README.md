# micro-chat

A tiny little command-line chat written in Python with SocketIO and Eventlet.

## Running/using:

Python >= 3.7 is required.

Clone this repo into a folder somewhere.

Install all dependencies:
```
pip3 install -r requirements.txt
```

To run a server, run
```
python3 -m micro_chat -s
```

To run a client, run
```
python3 -m micro_chat -c
```

## `scripts` directory

This directory contains batch/shell scripts for auxilliary program actions like building into an executable.

#### The `packaged` subdirectory

This directory contains scripts that are packaged with the executable for distribution.

## SocketIO event names

#### `send`

Emitted from client to send message to server.

Data format:
```{sender : <string> (must correspond to username in username table), content : <string>}```

#### `new_message`

Emitted from server to push send messages to clients.

Data format:
```{sender : <string>, content : <string>}```

#### `user_joined`

Emitted from the server to notify clients of a new user.

Data format:
```{username : <string>}```

#### `user_left`

Emitted from the server to notify clients of a user leaving

Data format:
```{username : <string>}```