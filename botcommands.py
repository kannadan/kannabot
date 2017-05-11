# -*- coding: utf-8 -*-

command_dict = {}


class Hello:

    def main( self, irc, line ):

        irc.send( 'PRIVMSG %s :Hello world!' % line[2] )

command_dict[ ':!hello' ] = Hello()

class Quit:

    def main( self, irc , line ):

        # määritellään komento vain pääkäyttäjille

        if line[0] in irc.users:

            irc.send( 'QUIT' )
            irc.socket.close()
            irc.done = 1
command_dict[ ':!quit' ] = Quit()

class Say:

    def main(self, irc, msg):
        irc.send('PRIVMSG %s :%s' % ("#otit.place", msg))

command_dict[ ':!say' ] = Say()