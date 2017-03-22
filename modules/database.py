'''
(C) Ryan Schaefer 2017
Handles processing of requests
'''
import os
def send_message(socketobj, message):
    'Sends a str as bytes through socket'
    message = message.encode()
    socketobj.sendall(message)
def handle(socket, payload):
    'Reads a request from a client'
    if 'CreateUser' in list(payload):
        if not os.path.isfile(os.path.join('users', payload['CreateUser'])):
            open(os.path.join('users', payload['CreateUser']), 'w').write('')
            send_message(socket, 'true')
