# -*- coding: utf-8 -*-

command_dict = {}
import socket
import time
import os

Channel = "#otit.place"
floodtime = 2

class Hello:

    def main( self, irc, line ):

        irc.send( 'PRIVMSG %s :Hello world :D' % line[2] )

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
        irc.send('PRIVMSG %s :%s' % (Channel, msg))

command_dict[ ':!say' ] = Say()

class Piirra:

    def main(self, irc, msg):
        files = []
        for file in os.listdir("."):
            if file.endswith(".txt"):
                files.append(file[:-4])
        if len(msg) == 5 and msg[4] == "-help":
            irc.send('PRIVMSG %s :%s' % (Channel, "!piirra <name of drawing> <starting x> <starting y>"))
            irc.send('PRIVMSG %s :%s' % (Channel, "-show shows a list of drawings"))
        elif len(msg) == 5 and msg[4] == "-show":
            irc.send('PRIVMSG %s :%s' % (Channel, files))

        elif len(msg) != 7:       #if not enough stuff
            irc.send('PRIVMSG %s :%s' % (Channel, "maby !piirra -help"))
        elif not isInt(msg[5]) or not isInt(msg[6]):    # if numbers not numbers
            irc.send('PRIVMSG %s :%s' % (Channel, "!piirra cordinates must be numbers"))
        elif int(msg[5]) > 53 or int(msg[5]) < 0 or int(msg[6]) > 71 or int(msg[6]) < 0:   #if numbers not on screen
            irc.send('PRIVMSG %s :%s' % (Channel, "!piirra drawing isn't on the screen"))
        else:
            if msg[4] in files:
                file = open(("%s.txt" %msg[4]), "r")
                moves = []
                send = 1
                for line in file:
                    line = line.split(" ")
                    coordinates = line[0].split("-")
                    x = int(coordinates[0]) + int(msg[5])
                    y = int(coordinates[1]) + int(msg[6])
                    if x > 54 or y > 71:
                        send = 0
                        irc.send('PRIVMSG %s :%s' % (Channel, "!piirra, Drawing doesn't fit. gimme better cordinates"))
                        break
                    else:
                        moves.append("%d-%d %s" %(x,y, line[1]))
                file.close()
                if send:
                    for i in range(len(moves)):
                        irc.send('PRIVMSG %s :%s' % (Channel, moves[i]))
                        time.sleep(floodtime)
            else:
                irc.send('PRIVMSG %s :%s' % (Channel, "!piirra, files: %s" % files))

command_dict[ ':!piirra' ] = Piirra()

class Help():

    def main(self, irc, line):
        irc.send('PRIVMSG %s :%s' % (Channel, "!piirra draws pictures"))
        irc.send('PRIVMSG %s :%s' % (Channel, "!hello, cheers you up"))

command_dict[ ':!help' ] = Help()

def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False