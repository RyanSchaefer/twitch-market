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
SERVER.send(dumps({'Start':''}))
while 1:
    PAYLOAD = SERVER.recv(2048)
    if 'Whisper' in PAYLOAD.keys():
        if match(r':(\w+)!\w+@.+:(.+)\r\n', PAYLOAD['Whisper']):
            USER = search(r':(\w+)!\w+@.+:(.+)\r\n', PAYLOAD['Whisper']).group(1)
            MESS = search(r':(\w+)!\w+@.+:(.+)\r\n', PAYLOAD['Whisper']).group(2)
            if '!send' in MESS:
                SERVER.send(dumps({'Send': 'MESS'}))
        