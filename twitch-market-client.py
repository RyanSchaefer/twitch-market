'''
Client processes messages from twitch
'''
from json import loads, dumps
from re import match, search
import socket
import modules
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
def whisper_handle(user, mess, serversocket):
    'Handle one whisper, makes connections to DB if needed'
    if '!createuser' in mess:
        send_message(serversocket, \
         dumps({'Database': {'Request': 'CreateUser', 'Username': 'test'}}))
def server_handle(serversocket):
    'Handles messages to and from SERVER'
    while 1:
        payload = loads(recv_message(serversocket))
        if 'Whisper' in list(payload):
            if match(r':(\w+)!\w+@.+:(.+)\r\n', payload['Whisper']):
                username = search(r':(\w+)!\w+@.+:(.+)\r\n', payload['Whisper']).group(1)
                message = search(r':(\w+)!\w+@.+:(.+)\r\n', payload['Whisper']).group(2)
                whisper_handle(username, message, serversocket)
server_handle(SERVER)
