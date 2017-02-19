<<<<<<< HEAD
'''
Handles messages to and from twich
Directs them to clients
'''
import multiprocessing
import socket
import re
import json
from BotPass import PASSWORD
def send_message(socketobj, message):
    'Sends a str as bytes through socket'
    message = message.encode()
    socketobj.sendall(message)
def recv_message(socketobj):
    'Recives a str as bytes though socket'
    return socketobj.recv(2048).decode()
class Server:
    'Handles recieving messages from twitch and directs messages from clients'
    twitch_socket = socket.socket()
    twitch_socket.connect(('irc.chat.twitch.tv', 6667))
    send_message(twitch_socket, 'PASS %s\r\n' % (PASSWORD))
    send_message(twitch_socket, 'NICK %s\r\n' % ('squid_coin_bot'))
    send_message(twitch_socket, 'JOIN #jtv\r\n')
    send_message(twitch_socket, 'CAP REQ :twitch.tv/commands\r\n')
    twitch_socket.recv(2048)
    twitch_socket.recv(2048)
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('', 9999))
    work_queue = multiprocessing.Queue()
    worker_queue = multiprocessing.Queue()
    whisper_queue = multiprocessing.Queue()
    def start():
        'Start the server'
        accept_process = multiprocessing.Process(target=Server.accept_connections)
        accept_process.daemon = True
        accept_process.start()
        recieve_process = multiprocessing.Process(target=Server.recieve_from_twitch)
        recieve_process.daemon = True
        recieve_process.start()
    def accept_connections():
        'accept all incoming connections, close ones not on local netowork'
        print('Accepting connections.')
        Server.server_socket.listen(10)
        while 1:
            (clientsocket, clientaddr) = Server.server_socket.accept()
            if re.match(r'192\.168\.\d{1,3}\.\d{1,3}', clientaddr[0])\
             or clientaddr[0] == '127.0.0.1':
                Server.worker_queue.put(clientsocket)
            else:
                clientsocket.close()
    def recieve_from_twitch():
        'recieve whispers from twitch'
        print('Recieving whispers.')
        while 1:
            message = recv_message(Server.twitch_socket)
            print(message)
            if message == 'PING :tmi.twitch.tv\r\n':
                send_message(Server.twitch_socket, 'PONG :tmi.twitch.tv\r\n')
            else:
                Server.work_queue.put({'Whisper': message})
    def connection_handle(connection):
        'Handles a back and forth of a connection'
        send_message(connection, json.dumps(Server.work_queue.get()))
        payload = json.loads(recv_message(connection))
        if 'Send' in list(payload):
            Server.whisper_queue.put(payload)
    def handout_work():
        'Giving work out to clients for them to process'
        print('Handing out work.')
        while 1:
            if not Server.worker_queue.empty and not Server.work_queue.empty:
                connection = Server.worker_queue.get()
                handle = multiprocessing.Process(target=Server.connection_handle, \
                  args=(connection,))
                handle.daemon = True
                handle.start()
if __name__ == '__main__':
    Server.start()
    input()
=======
'''
(C) Ryan Schaefer 2017
Handles connections that attempt to modify the database
Also handles connections from and to twitch
'''
from threading import Thread
from Queue import Queue
from re import match
import socket
from json import dumps, loads
from BotPass import PASSWORD
from time import sleep
class TwitchMarketServer(object):
    'Main module'
    def __init__(self):
        self.queue = Queue()
        self.work_queue = Queue()
        self.whisper_queue = Queue()
        self.server_socket = socket.socket()
        self.server_socket.bind(('127.0.0.1', 9999))
        self.twitch_socket = socket.socket()
        self.twitch_socket.connect(('irc.chat.twitch.tv', 6667))
        self.twitch_socket.send('PASS %s\r\n' % (PASSWORD))
        self.twitch_socket.send('NICK %s\r\n' % ('squid_coin_bot'))
        self.twitch_socket.send('JOIN #jtv\r\n')
        self.twitch_socket.send('CAP REQ :twitch.tv/commands\r\n')
        print self.twitch_socket.recv(2048)
        print self.twitch_socket.recv(2048)
    def start_server(self):
        'starts required threads as daemons'
        accept_thread = Thread(target=self.accept_connections)
        accept_thread.daemon = True
        accept_thread.start()
        handler_thread = Thread(target=self.connection_handler)
        handler_thread.daemon = True
        handler_thread.start()
        recieve_thread = Thread(target=self.recieve_whispers)
        recieve_thread.daemon = True
        recieve_thread.start()
        send_thread = Thread(target=self.send_whispers)
        send_thread.daemon = True
        send_thread.start()
    def accept_connections(self):
        'accept incoming connections'
        self.server_socket.listen(10)
        while 1:
            (clientsocket, clientaddr) = self.server_socket.accept()
            if match(r'192\.168\.\d{1,3}\.\d{1,3}', clientaddr[0]) or clientaddr[0] == '127.0.0.1':
                self.queue.put(clientsocket)
            else:
                clientsocket.close()
    def connection_handler(self):
        'directs all connections that are currently connected'
        while 1:
            if self.work_queue.unfinished_tasks > 0:
                work = self.work_queue.get()
                connection = Thread(target=self.process_connections, args=(self.queue.get(), work))
                connection.daemon = True
                connection.start()
    def process_connections(self, connection, work):
        'figure out what the connections data is saying'
        connection.send(work)
        payload = connection.recv(2048)
        print payload
        payload = loads(payload)
        if 'Start' in payload.keys():
            pass
        elif 'Send' in payload.keys():
            self.whisper_queue.put(payload['Send'])
        elif 'Pass' in payload.keys():
            pass
        elif 'End' in payload.keys():
            return False
        self.queue.put(connection)
    def recieve_whispers(self):
        'connection from server to twitch'
        while 1:
            work = self.twitch_socket.recv(2048)
            print work
            self.work_queue.put(dumps({'Whisper': work}))
    def send_whispers(self):
        'Send a whisper on twitch'
        while 1:
            whisper = self.whisper_queue.get()
            self.twitch_socket.send('PRIVMSG #jtv :.w %s %s\r\n' % \
             (whisper['Username'], whisper['Message']))
            sleep(1.8)
TwitchMarketServer().start_server()
print 'Server started'
input()
>>>>>>> 537111db82795cf69f71f7fa077b4ca8e019c872
