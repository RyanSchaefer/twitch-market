'''
Client processes messages from twitch
'''
from json import loads, dumps
from re import match, search
import socket
SERVER = socket.socket()
SERVER.connect(('127.0.0.1', 9999))
print('connected')
def send_message(socketobj, message):
    'Sends a str as bytes through socket'
    message = message.encode()
    socketobj.sendall(message)
def recv_message(socketobj):
    'Recives a str as bytes though socket'
    return socketobj.recv(2048).decode()
send_message(SERVER, dumps({'Start':''}))
while 1:
    PAYLOAD = SERVER.recv(2048)
    if 'Whisper' in PAYLOAD.keys():
        if match(r':(\w+)!\w+@.+:(.+)\r\n', PAYLOAD['Whisper']):
            USER = search(r':(\w+)!\w+@.+:(.+)\r\n', PAYLOAD['Whisper']).group(1)
            MESS = search(r':(\w+)!\w+@.+:(.+)\r\n', PAYLOAD['Whisper']).group(2)
            if '!send' in MESS:
                send_message(SERVER, dumps({'Send': (USER, MESS)}))
<<<<<<< HEAD
                
=======
>>>>>>> 537111db82795cf69f71f7fa077b4ca8e019c872
