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
import threading
import Queue
import sys


class kannabot:

    def __init__(self):

        self.users = [':kannadan!kannadan@otitsun.oulu.fi']

        #address stuff for irc
        self.server = 'irc.oulu.fi'
        self.port = 6667
        self.username = 'kannabot'
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
        self.portS = 2015  # Reserve a port for your service.
        self.conn = None
        self.messages = Queue.Queue()
        self.socks = []

        self.socketdummy1 = socket.socket()
        self.socketdummy2 = socket.socket()


    def send(self, string):

        self.socket.send(string + '\r\n')

    def connect(self):

        self.socket.connect((self.server, self.port))
        self.send('NICK %s' % self.nick)
        self.send('USER %s a a :%s' % (self.username, self.realname))
        self.send('JOIN %s' % self.channel)
        self.soc.bind((self.host, self.portS))
        self.soc.listen(5)

        self.socketdummy2.bind((socket.gethostname(), 2016))
        self.socketdummy2.listen(1)


    def connectGUI(self):
        print("Gui listener active")
        self.socketdummy1.connect((socket.gethostname(), 2016))
        while not self.done:
            self.conn, addr = self.soc.accept()
            print("Connected to user")
            self.socks.append(self.conn)
            self.socketdummy1.send("staph")
        self.socketdummy1.close()
        self.socketdummy2.close()





    def check(self, line):

        print line

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

    def listener(self):
        print("listener active")
        self.socks.append(self.socket)
        connd, add = self.socketdummy2.accept()
        self.socks.append(connd)

        while not self.done:
            ready_socks, _, _ = select.select(self.socks, [], [])
            for sock in ready_socks:
                try:
                    data, addr = sock.recvfrom(1024)
                    data = data.split('\r\n')
                    for line in data:
                        if line != "" and line != " ":
                            self.messages.put(line)
                except socket.error:        #if connection is lost. mostly for the GUI
                    self.socks.remove(sock)
            if len(self.socks) == o:
                self.done = 1


    def speaker(self):
        lastmsg = 0
        print("speaker active")
        while not self.done:
            line = self.messages.get()
            self.messages.task_done()
            print (line)
            line = line.split(" ")
            if line[0][2:7] == "!move":
                print ("made a move")
                print ("%s-%s %s" % (line[1], line[3], line[4]))
                if time.time() - lastmsg >= 1:
                    lastmsg = time.time()
                    self.commands[':!say'].main(self, "%s-%s %s" % (line[1], line[3], line[4]))
                else:
                    time.sleep(1)
                    self.commands[':!say'].main(self, "%s-%s %s" % (line[1], line[3], line[4]))
                    lastmsg = time.time()
            self.check(line)
        sys.exit()



    def mainloop(self):

        thread1 = threading.Thread(target=self.speaker)
        thread2 = threading.Thread(target=self.listener)
        thread3 = threading.Thread(target=self.connectGUI)
        thread1.start()
        thread2.start()
        thread3.start()



if __name__ == '__main__':
    irc = kannabot()
    irc.connect()
    irc.mainloop()