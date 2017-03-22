'''
(C) Ryan Schaefer 2017
Stores user information
Respondes to requests from server and clients
'''
import multiprocessing
import os
import socket
import json
import re
import modules
def send_message(socketobj, message):
    'Sends a str as bytes through socket'
    message = message.encode()
    socketobj.sendall(message)
def recv_message(socketobj):
    'Recives a str as bytes though socket'
    return socketobj.recv(2048).decode()
def accept_thread(serversocket, db_queue):
    'Accepts connections to the database'
    serversocket.listen(10)
    while 1:
        (clientsocket, clientaddr) = serversocket.accept()
        if re.match(r'192\.168\.\d{1,3}\.\d{1,3}', clientaddr[0]) \
          or clientaddr[0] == '127.0.0.1':
            payload = json.loads(recv_message(clientsocket))
            db_queue.put((clientsocket, payload))
        else:
            clientsocket.close()
def database_handler(db_queue):
    'Handles requests from clients in a linear fashion'
    while 1:
        csocket, payload = db_queue.get()
        modules.database.handle(csocket, payload)
def start(serversocket, db_queue):
    'start the server'
    multiprocessing.Process(target=accept_thread, args=(serversocket, db_queue)).start()
    multiprocessing.Process(target=database_handler, args=(db_queue,)).start()
if __name__ == '__main__':
    SERVER = socket.socket()
    SERVER.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    SERVER.bind(('127.0.0.1', 9988))
    M = multiprocessing.Manager()
    M.queue = M.Queue()
    start(SERVER, M.queue)
    print('Server Started.')
    input()
