'''
(C) Ryan Schaefer 2017
Handles connections that attempt to modify the database
Also handles connections from and to twitch
'''
from threading import Thread
from Queue import Queue
from re import match
import socket
from BotPass import PASSWORD
class TwitchMarketServer(object):
    'Main module'
    def __init__(self):
        self.queue = Queue()
        self.workqueue = Queue()
        self.serversocket = socket.socket()
        self.serversocket.bind(("127.0.0.1", 9999))
        self.twitchsocket = socket.socket()
        self.twitchsocket.connect(('irc.chat.twitch.tv', 6667))
        self.twitchsocket.send('PASS %s\r\n' % (PASSWORD))
        self.twitchsocket.send('NICK %s\r\n' % ('squid_coin_bot'))
        self.twitchsocket.send('JOIN #jtv\r\n')
        self.twitchsocket.send('CAP REQ :twitch.tv/commands\r\n')
    def start_server(self):
        'starts required threads as daemons'
        sendthread = Thread(target=self.accept_connections)
        sendthread.daemon = True
        sendthread.start()
        handlethread = Thread(target=self.connection_handler)
        handlethread.daemon = True
        handlethread.start()
    def accept_connections(self):
        'accept incoming connections'
        self.serversocket.listen(10)
        while 1:
            (clientsocket, clientaddr) = self.serversocket.accept()
            if match(r'192\.168\.\d{1,3}\.\d{1,3}', clientaddr[0]) or clientaddr[0] == "127.0.0.1":
                self.queue.put(clientsocket)
            else:
                clientsocket.close()
    def connection_handler(self):
        'directs all connections that are currently connected'
        while 1:
            Thread(target=self.process_connections, args=(self.queue.get(),)).start()
    def process_connections(self, connection):
        'figure out what the connections data is saying'
        print connection.recv(2048)
        connection.send(self.workqueue.get())
        self.queue.put(connection)
TwitchMarketServer().start_server()
print "Server started"
input()
