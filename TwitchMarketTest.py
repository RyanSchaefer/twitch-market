'''
(C) Ryan Schaefer 2017
Handles messages between twich and client
Doesn't establish a connection to twitch
'''
import multiprocessing
import socket
import re
import json
from time import sleep
from BotPass import PASSWORD
from UnitTest import TEST
def send_message(socketobj, message):
    'Sends a str as bytes through socket'
    message = message.encode()
    socketobj.sendall(message)
def recv_message(socketobj):
    'Recives a str as bytes though socket'
    return socketobj.recv(2048).decode()
def accept_connections(server_socket, worker_queue):
    'accept all incoming connections, close ones not on local netowork'
    print('Accepting connections.')
    server_socket.listen(10)
    while 1:
        (clientsocket, clientaddr) = server_socket.accept()
        if re.match(r'192\.168\.\d{1,3}\.\d{1,3}', clientaddr[0])\
            or clientaddr[0] == '127.0.0.1':
            print('Client connected from: %s:%s' % clientaddr)
            worker_queue.put(clientsocket)
        else:
            clientsocket.close()
def connection_handle(work_queue, worker_queue, whisper_queue, connection):
    'Handles a back and forth of a connection'
    send_message(connection, json.dumps(work_queue.get()))
    payload = json.loads(recv_message(connection))
    print(payload)
    if 'Send' in list(payload):
        whisper_queue.put(tuple(payload['Send']))
    elif 'End' in list(payload):
        return True
    worker_queue.put(connection)

def handout_work(work_queue, worker_queue, whisper_queue):
    'Gives work out to clients for them to process'
    print('Handing out work.')
    while 1:
        if not worker_queue.empty() and not work_queue.empty():
            connection = worker_queue.get()
            multiprocessing.Process(target=connection_handle, \
                args=(work_queue, worker_queue, whisper_queue, connection)).start()
def start(work_queue, worker_queue, whisper_queue, server_socket):
    for test in TEST:
        work_queue.put(test)
    
if __name__ == '__main__':
    pass
