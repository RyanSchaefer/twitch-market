'''
Client processes messages from twitch
'''
from json import loads, dumps
from re import match, search
import socket
import commands
SERVER = socket.socket()
SERVER.connect(('127.0.0.1', 9999))
DB = socket.socket()
DB.connect(('127.0.0.1', 9988))
print('connected')
def send_message(socketobj, message):
    'Sends a str as bytes through socket'
    message = message.encode()
    socketobj.sendall(message)
def recv_message(socketobj):
    'Recives a str as bytes though socket'
    return socketobj.recv(2048).decode()
def whisper_handle(user, mess, serversocket, database):
    'Handle one whisper, makes connections to DB if needed'
    commands.handle(user, mess, serversocket, database)
def server_handle(serversocket, dbsocket):
    'Handles messages to and from SERVER'
    while 1:
        payload = loads(recv_message(serversocket))
        print(payload)
        if 'Whisper' in list(payload):
            if match(r':(\w+)!\w+@.+:(.+)\r\n', payload['Whisper']):
                username = search(r':(\w+)!\w+@.+:(.+)\r\n', payload['Whisper']).group(1)
                message = search(r':(\w+)!\w+@.+:(.+)\r\n', payload['Whisper']).group(2)
                print("%s:%s" % (username, message))
                whisper_handle(username, message, serversocket, dbsocket)
                print('Message sent')
            else:
                send_message(serversocket, dumps({'Pass': ''}))
        else:
            send_message(serversocket, dumps({'Pass': ''}))
server_handle(SERVER, DB)
