# micro-chat

A tiny little command-line chat written in Python with SocketIO and Eventlet.

## Running/using:

Python >= 3.7 is required.

Clone this repo into a folder somewhere.

Install dependencies for running server:
```
pip3 install -r requirements-server.txt
```

Install dependencies for running client:
```
pip3 install -r requirements-client.txt
```

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