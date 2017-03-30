'''
(C) Ryan Schaefer 2017
Handles messages between twich and client
'''
import multiprocessing
import socket
import re
import json
from time import sleep
from BotPass import PASSWORD
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
def recieve_from_twitch(work_queue, twitch_socket):
    'recieve whispers from twitch'
    print('Recieving whispers.')
    while 1:
        message = recv_message(twitch_socket)
        print(message)
        if message == 'PING :tmi.twitch.tv\r\n':
            send_message(twitch_socket, 'PONG :tmi.twitch.tv\r\n')
        else:
            work_queue.put({'Whisper': message})
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
def send_whispers(whisper_queue, twitch_socket):
    'Sends whispers to users on twitch'
    while 1:
        if not whisper_queue.empty():
            args = whisper_queue.get()
            send_message(twitch_socket, 'PRIVMSG #jtv :.w %s %s\r\n' % args)
            sleep(1.6)
def start(work_queue, worker_queue, whisper_queue, server_socket, twitch_socket):
    'Start the server'
    multiprocessing.Process(target=accept_connections, \
        args=(server_socket, worker_queue)).start()
    multiprocessing.Process(target=recieve_from_twitch, \
        args=(work_queue, twitch_socket)).start()
    multiprocessing.Process(target=handout_work, \
        args=(work_queue, worker_queue, whisper_queue)).start()
    multiprocessing.Process(target=send_whispers, \
    args=(whisper_queue, twitch_socket)).start()
if __name__ == '__main__':
    MANAGER = multiprocessing.Manager()
    MANAGER.worker_queue = MANAGER.Queue()
    MANAGER.work_queue = MANAGER.Queue()
    MANAGER.whisper_queue = MANAGER.Queue()
    TWITCH = socket.socket()
    TWITCH.connect(('irc.chat.twitch.tv', 6667))
    send_message(TWITCH, 'PASS %s\r\n' % (PASSWORD))
    send_message(TWITCH, 'NICK %s\r\n' % ('squid_coin_bot'))
    send_message(TWITCH, 'JOIN #jtv\r\n')
    send_message(TWITCH, 'CAP REQ :twitch.tv/commands\r\n')
    TWITCH.recv(2048)
    TWITCH.recv(2048)
    SERVER = socket.socket()
    SERVER.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    SERVER.bind(('', 9999))
    start(MANAGER.work_queue, MANAGER.worker_queue, MANAGER.whisper_queue, \
     SERVER, TWITCH)
    input()
    