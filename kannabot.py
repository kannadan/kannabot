# -*- coding: utf-8 -*-

"""
    Commands
    !hello
    !quit
"""

import socket
import botcommands
import select
import time


class kannabot:

    def __init__(self):

        self.users = [':kannadan!kannadan@otitsun.oulu.fi']

        #address stuff for irc
        self.server = 'irc.oulu.fi'
        self.port = 6667
        self.username = 'kannadan'
        self.realname = '-'
        self.nick = 'kannabot'

        self.socket = socket.socket()

        #commands
        self.commands = botcommands.command_dict

        self.done = 0
        self.channel = '#kannabot'

        #socket to java GUI that sends coordinate messages to irc through kannabot

        self.soc = socket.socket()  # Create a socket object
        self.host = "localhost"  # Get local machine name
        self.portS = 2004  # Reserve a port for your service.
        self.soc.bind((self.host, self.portS))  # Bind to the port
        print ("socket ready")
        self.soc.listen(5)  # Now wait for client connection.

        self.conn, addr = self.soc.accept()  # Establish connection with client.

    def send(self, string):

        self.socket.send(string + '\r\n')

    def connect(self):

        self.socket.connect((self.server, self.port))
        self.send('NICK %s' % self.nick)
        self.send('USER %s a a :%s' % (self.username, self.realname))
        self.send('JOIN %s' % self.channel)

    def check(self, line):

        print line
        line = line.split(' ')

        # respond to ping
        if line[0] == 'PING':
            self.send('PONG :abc')



        try:

            # private messages

            if line[2][0] != '#':
                line[2] = line[0].split('!')[0][1:]

            # do a thing
            self.commands[line[3]].main(self, line)

        except:

            pass

    def mainloop(self):

        buffer = ''
        socks = [self.conn, self.socket]
        moves = []
        waitStart = 0

        while not self.done:

            ready_socks, _, _ = select.select(socks, [], [])
            for sock in ready_socks:
                data, addr = sock.recvfrom(1024)  # This is will not block
                data = data.split('\r\n')
                for line in data:
                    if line[2:7] == "!move":
                        print ("made a move")
                        print ("%s-%s %s" % (line[1], line[3], line[4]))
                        if time.time() - waitStart >= 1:
                            waitStart = time.time()
                            self.commands[':!say'].main(self, "%s-%s %s" % (line[1], line[3], line[4]))
                        else:
                            moves.insert(0, "%s-%s %s" % (line[1], line[3], line[4]))
                    self.check(line)
            for i in range(len(moves)):
                if time.time() - waitStart >= 1:
                    waitStart = time.time()
                    self.commands[':!say'].main(self, "%s-%s %s" % (line[1], line[3], line[4]))
                else:
                    time.sleep(1)
                    waitStart = time.time()
                    self.commands[':!say'].main(self, "%s-%s %s" % (line[1], line[3], line[4]))


            """
            buffer += self.socket.recv(4096)
            buffer = buffer.split('\r\n')

            for line in buffer[0:-1]:
                self.check(line)

            buffer = buffer[-1]

            print ("java check")
            msg = self.conn.recv(1024)
            self.commands[':!say'].main(self, msg[2:])
            print (msg[2:])"""

if __name__ == '__main__':
    irc = kannabot()
    irc.connect()
    irc.mainloop()