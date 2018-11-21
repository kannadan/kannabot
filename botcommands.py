# -*- coding: utf-8 -*-

command_dict = {}
import socket
import time
import os
from PIL import Image
import pictures

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
        photos = []
        for file in os.listdir("."):
            if file.endswith(".txt"):
                files.append(file[:-4])
            elif file.endswith(".png"):
                photos.append(file[:-4])
        if len(msg) == 5 and msg[4] == "-help":
            irc.send('PRIVMSG %s :%s' % (Channel, "!piirra <name of drawing> <starting x> <starting y>"))
            irc.send('PRIVMSG %s :%s' % (Channel, "-show shows a list of drawings"))
        elif len(msg) == 5 and msg[4] == "-show":
            irc.send('PRIVMSG %s :%s' % (Channel, files))

        elif not isInt(msg[5]) or not isInt(msg[6]):    # if numbers not numbers
            irc.send('PRIVMSG %s :%s' % (Channel, "!piirra cordinates must be numbers"))
        elif int(msg[5]) > 53 or int(msg[5]) < 0 or int(msg[6]) > 71 or int(msg[6]) < 0:   #if numbers not on screen
            irc.send('PRIVMSG %s :%s' % (Channel, "!piirra drawing isn't on the screen"))
        elif len(msg) == 7 or len(msg) == 9 or len(msg) == 10 or len(msg) == 11:
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

            elif msg[4] in photos:
                file = Image.open(("%s.png" %msg[4]))
                moves = []
                send = 1
                if len(msg) == 9:
                    width = int(msg[7])
                    height = int(msg[8])
                elif len(msg) == 10:
                    width = int(msg[7])
                    height = int(msg[8])
                    if msg[9] == "true":
                        invert = 1
                    else:
                        invert = 0
                elif len(msg) == 11:
                    width = int(msg[7])
                    height = int(msg[8])
                    if msg[9] == "true":
                        invert = 1
                    else:
                        invert = 0
                    if msg[10] == "1":
                        black = 1
                    else:
                        black = 0
                else:
                    width = 0
                    height = 0
                    invert = 0
                    black = 0
                img = pictures.resize(file, width, height)
                ix, iy = img.size
                startx = int(msg[5])
                starty = int(msg[6])
                x = ix + int(msg[5])
                y = iy + int(msg[6])
                if x > 54 or y > 71:
                    send = 0
                    irc.send('PRIVMSG %s :%s' % (Channel, "!piirra, Drawing doesn't fit. gimme better cordinates"))
                else:
                    img = pictures.colorize(img, invert, black)
                    for y2 in range(iy):
                        for x2 in range(ix):
                            moves.append("%d-%d %s" %(x2+startx,y2+starty, img[y2][x2]))
                file.close()

                if send:
                    for i in range(len(moves)):
                        message = 'PRIVMSG %s :%s' % (Channel, moves[i])
                        irc.send(message)
                        time.sleep(2)
                else:
                    irc.send('PRIVMSG %s :%s' % (Channel, "!piirra, files: %s" % files))
        elif len(msg) != 7 or len(msg) :       #if not enough stuff
            irc.send('PRIVMSG %s :%s' % (Channel, "maby !piirra -help"))

command_dict[ ':!piirra' ] = Piirra()

class Help():

    def main(self, irc, line):
        irc.send('PRIVMSG %s :%s' % (Channel, "!piirra draws pictures"))
        irc.send('PRIVMSG %s :%s' % (Channel, "!hello, cheers you up"))

command_dict[ ':!help' ] = Help()

class Save():

    def main(self, irc, line):

        if len(line) == 5:
            username = line[0].split("!")
            username = username[0]
            if username not in irc.saving:
                name = line[4]
                irc.saving[username] = [name]
                irc.send('PRIVMSG %s :%s' % (Channel, "Saving"))

        else:
            irc.send('PRIVMSG %s :%s' % (Channel, "!save <file name>"))

command_dict[':!save'] = Save()

class Done():

    def main(self, irc, line):

        username = line[0].split("!")
        username = username[0]
        if username in irc.saving:
            print "username checks out"
            moves = irc.saving[username]
            name = irc.checkName(moves[0])
            del moves[0]
            xMin = 53
            yMin = 71
            for i in range(len(moves)):
                jono = moves[i].split(" ")
                jono = jono[0].split("-")
                x = int(jono[0])
                y = int(jono[1])
                if x < xMin:
                    xMin = x
                if y < yMin:
                    yMin = y

            for i in range(len(moves)):
                jono = moves[i].split(" ")
                color = jono[1]
                jono = jono[0].split("-")
                x = int(jono[0])
                y = int(jono[1])
                x = x-xMin
                y = y-yMin
                moves[i] = "%d-%d %s" %(x, y, color)
            file = open(("%s.txt" %name), "w")
            for i in range(len(moves)):
                file.write("%s\n" % moves[i])
            file.close()
            irc.send('PRIVMSG %s :%s' % (Channel, "picture saved"))
            irc.doneFiles.append(name)
            del irc.saving[username]

        else:
            irc.send('PRIVMSG %s :%s' % (Channel, "You are not saving anything"))

command_dict[':!done'] = Done()

def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
