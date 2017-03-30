'''
(C) Ryan Schaefer 2017
Handles messages between twich and client
Doesn't establish a connection to twitch
'''
import multiprocessing
import socket
import re
import json
import UnitTest
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
    elif 'Pass' in list(payload):
        pass
    worker_queue.put(connection)

def handout_work(work_queue, worker_queue, whisper_queue):
    'Gives work out to clients for them to process'
    print('Handing out work.')
    while 1:
        if not worker_queue.empty() and not work_queue.empty():
            connection = worker_queue.get()
            print('handing out work to connection')
            multiprocessing.Process(target=connection_handle, \
                args=(work_queue, worker_queue, whisper_queue, connection)).start()

def print_whispers(whisper_queue):
    while 1:
        if not whisper_queue.empty:
            print('%s:%s' % (whisper_queue.get()))

def start(work_queue, worker_queue, whisper_queue, server_socket):
    multiprocessing.Process(target=accept_connections, \
        args=(server_socket, worker_queue)).start()
    multiprocessing.Process(target=handout_work, \
        args=(work_queue, worker_queue, whisper_queue)).start()
    multiprocessing.Process(target=print_whispers, \
    args=(whisper_queue,)).start()

if __name__ == '__main__':
    MANAGER = multiprocessing.Manager()
    MANAGER.worker_queue = MANAGER.Queue()
    MANAGER.work_queue = MANAGER.Queue()
    MANAGER.whisper_queue = MANAGER.Queue()
    SERVER = socket.socket()
    SERVER.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    SERVER.bind(('127.0.0.1', 9999))
    start(MANAGER.work_queue, MANAGER.worker_queue, MANAGER.whisper_queue, SERVER)
    for test in UnitTest.TEST:
        MANAGER.work_queue.put({'Whisper': test})
    input()
