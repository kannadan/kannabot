# -*- coding: utf-8 -*-

command_dict = {}
import socket
import time

class Hello:

    def main( self, irc, line ):

        irc.send( 'PRIVMSG %s :Hello world!' % line[2] )

command_dict[ ':!hello' ] = Hello()

class Quit:

    def main( self, irc , line ):

        # usr has to be main one

        if line[0] in irc.users:

            irc.send( 'QUIT' )
            socket.socket().connect((irc.host, irc.portS))
            irc.done = 1
            irc.socket.close()
            irc.soc.close()
            print ("quit")

command_dict[ ':!quit' ] = Quit()

class Say:

    def main(self, irc, msg):
        irc.send('PRIVMSG %s :%s' % ("#kannabot", msg))

command_dict[ ':!say' ] = Say()

class Piirra:

    def main(self, irc, msg):
        file = open(("%s.txt" %msg[4]), "r")
        for line in file:
            irc.send('PRIVMSG %s :%s' % ("#kannabot", line))
            time.sleep(2)


command_dict[ ':!piirra' ] = Piirra()