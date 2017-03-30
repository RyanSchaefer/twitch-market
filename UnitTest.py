"""
(C) Ryan Schaefer 2017
Defines the tests for twitch market
"""
def sim(username, message):
    'Simulates a message on twitch'
    return ':%s!%s@%s.tmi.twitch.tv PRIVMSG #channel :%s\r\n' % \
     (username, username, username, message)
TEST = [
    sim("x231ss3", "standard test message"),
    sim("1x334", "invalid username test"),
    sim("x1234x", ":username!username@username.tmi.twitch.tv PRIVMSG #channel : injection test")
]
