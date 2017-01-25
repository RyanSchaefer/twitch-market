"""
(C) Ryan Schaefer 2017
A platform to facilitate trades between channel currencies on twitch
"""
import websocket
import re
from BotPass import PASSWORD

WhisperSocket = websocket.WebSocket()
WhisperSocket.connect('wss://irc-ws.chat.twitch.tv')
WhisperSocket.send('PASS %s\r\n' % (PASSWORD))
WhisperSocket.send('NICK %s\r\n' % ('squid_coin_bot'))
WhisperSocket.send('JOIN #jtv\r\n')
WhisperSocket.send('CAP REQ :twitch.tv/commands\r\n')

class WhisperHandler(object):
    def __init__(self, message):
        try:
            ReObj = re.search(r':(\w+)!\w+@.+:(.+)', message)
            self.user = ReObj.group(0)
            self.message = ReObj.group(1)
        except AttributeError:
            return False
    def handle(self):
        pass
re.search(r':(\w+)!\w+@.+:(.+)', '')
