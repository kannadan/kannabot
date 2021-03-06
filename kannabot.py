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
import os


class kannabot:

    def __init__(self):

        self.users = [':kannadan!kannadan@otitsun.oulu.fi']

        #address stuff for irc
        self.server = 'irc.oulu.fi'
        self.port = 6667
        self.username = 'kannabot'
        self.realname = '-'
        self.nick = 'kannabot'
        self.floodtime = 2

        self.socket = socket.socket()

        #commands
        self.commands = botcommands.command_dict

        self.done = 0
        self.channel = '#otit.place'

        #socket to java GUI that sends coordinate messages to irc through kannabot
        """
        self.soc = socket.socket()  # Create a socket object
        self.host = "127.0.0.1"
        self.portS = 5014  # Reserve a port for your service.
        self.conn = None

        self.socketdummy1 = socket.socket()
        self.socketdummy2 = socket.socket()
        """
        self.messages = Queue.Queue()
        self.socks = []
        self.files = {}
        self.doneFiles = []

        for file in os.listdir("."):
            if file.endswith(".txt"):
                self.doneFiles.append(file[:-4])

        self.saving = {}

        self.colors = ["black", "white", "red", "blue", "yellow", "cyan", "magenta", "green"]

    def send(self, string):

        self.socket.send(string + '\r\n')

    def connect(self):

        self.socket.connect((self.server, self.port))
        self.send('NICK %s' % self.nick)
        self.send('USER %s a a :%s' % (self.username, self.realname))
        self.send('JOIN %s' % self.channel)
        """self.soc.bind((self.host, self.portS))
        self.soc.listen(5)

        self.socketdummy2.bind((socket.gethostname(), 2016))
        self.socketdummy2.listen(1)"""


    def connectGUI(self):
        print("Gui listener active")
        self.socketdummy1.connect((socket.gethostname(), 2016))
        while not self.done:
            self.conn, addr = self.soc.accept()
            print("Connected to user")
            #self.socks.append(self.conn)
            self.socketdummy1.send("staph")
        self.socketdummy1.close()
        self.socketdummy2.close()
        print ("Gui listener dead")





    def check(self, line):


        # respond to ping
        if line[0] == 'PING':
            self.send('PONG :abc')

        try:

            # private messages
            if "!Save" in line[0] or "!Save" in line[1]:
                line[3] = self.checkName(line[3])
                print("saving")
                if line[4] == "STAPH":
                    self.files[line[3]].write("%s %s\n" % (line[1], line[2]))
                    print ("CLOSING FILE")
                    self.files[line[3]].close()
                    del self.files[line[3]]
                    self.doneFiles.append(line[3])

                elif line[3] in self.files:
                    print("writing!!!")
                    print("%s %s \n" %(line[1], line[3]))
                    self.files[line[3]].write("%s %s\n" % (line[1], line[2]))
                else:
                    print ("OPENING FILE")
                    self.files[line[3]] = open(("%s.txt" % line[3]), "w")
                    self.files[line[3]].write("%s %s\n" % (line[1], line[2]))

            if len(line) == 5 and line[0].split("!")[0] in self.saving:
                if self.checkFormat(line[-2:]):
                    print ("saving to file")
                    name = line[0].split("!")
                    self.saving[name[0]].append("%s %s" % (line[3][1:], line[4]))

            if line[2][0] != '#':
                line[2] = line[0].split('!')[0][1:]

            # do a thing
            self.commands[line[3]].main(self, line)


        except Exception as e:
            print e
            pass

    def listener(self):
        print("listener active")
        self.socks.append(self.socket)
        #connd, add = self.socketdummy2.accept()
        #self.socks.append(connd)

        while not self.done:
            ready_socks, _, _ = select.select(self.socks, [], [])
            for sock in ready_socks:
                try:
                    data, addr = sock.recvfrom(1024)
                    print(data)
                    data = data.split('\r\n')
                    for line in data:
                        if line != "" and line != " ":
                            self.messages.put(line)
                except socket.error:        #if connection is lost. mostly for the GUI
                    self.socks.remove(sock)
                    sock.close()
            if len(self.socks) == 0:
                self.done = 1
        print("listener dead")


    def speaker(self):
        lastmsg = 0
        print("speaker active")
        while not self.done:
            line = self.messages.get()
            self.messages.task_done()
            line = line.split(" ")
            if line[0] == "!move":
                print ("made a move")
                print ("%s-%s %s\n" % (line[1], line[3], line[4]))
                if time.time() - lastmsg >= self.floodtime:
                    lastmsg = time.time()
                    self.commands[':!say'].main(self, "%s-%s %s" % (line[1], line[3], line[4]))
                else:
                    time.sleep(self.floodtime)
                    self.commands[':!say'].main(self, "%s-%s %s" % (line[1], line[3], line[4]))
                    lastmsg = time.time()
            self.check(line)
        print ("speaker dead")
        sys.exit()

    def checkName(self, name):
        if name in self.doneFiles:
            name = "%s_" % name
            name = self.checkName(name)
        return name

    def checkFormat(self, line):
        print "checking format"
        if "-" in line[0]:
            cordinates = line[0].split("-")
            if len(cordinates) == 2:
                cordinates = cordinates[0].split(":")[1], cordinates[1]
                if botcommands.isInt(cordinates[0]) and botcommands.isInt(cordinates[1]):
                    print cordinates
                    x = int(cordinates[0])
                    y = int (cordinates[1])
                    if x < 54 and x >= 0 and y < 72 and y >= 0:
                        if line[1] in self.colors:
                            return True
        return False


    def mainloop(self):

        thread1 = threading.Thread(target=self.speaker)
        thread2 = threading.Thread(target=self.listener)
        #thread3 = threading.Thread(target=self.connectGUI)
        thread1.start()
        thread2.start()
        #thread3.start()



if __name__ == '__main__':
    irc = kannabot()
    irc.connect()
    irc.mainloop()
