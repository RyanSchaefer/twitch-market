'''
(C) Ryan Schaefer 2017
Handles a processing request from the server's queue
Can connect to Database to read from it
'''
from json import loads, dumps
from re import match, search
import socket
SERVER = socket.socket()
SERVER.connect(('127.0.0.1', 9999))
print 'connected'
def check_message():
    payload = loads(SERVER.recv(2048))
    print payload
    if 'Whisper' in payload.keys():
        if match(r':(\w+)!\w+@.+:(.+)\r\n', payload['Whisper']):
            user = search(r':(\w+)!\w+@.+:(.+)\r\n', payload['Whisper']).group(1)
            mess = search(r':(\w+)!\w+@.+:(.+)\r\n', payload['Whisper']).group(2)
            if '!send' in mess:
                SERVER.send(dumps({'Send': {'Username': user, 'Message': mess}}))
                return True
            SERVER.send(dumps({'Pass':''}))
while 1:
    check_message()
        