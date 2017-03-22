'''
(C) Ryan Schaefer 2017
Handles user commands
'''
import json
def send_message(socketobj, message):
    'Sends a str as bytes through socket'
    message = message.encode()
    socketobj.sendall(message)
def recv_message(socketobj):
    'Recives a str as bytes though socket'
    return socketobj.recv(2048).decode()
def handle(database, server, user, mess):
    'handles one message from a user'
    if '!createuser' in mess:
        send_message(database, json.dumps({'CreateUser': user}))
        response = json.loads(recv_message(database))
        if response:
            send_message(server, json.dumps({'Send':(user, 'User creation sucessful.')}))
        if not response:
            send_message(server, json.dumps({'Send':(user, 'User creation failed.')}))
