import irc3


@irc3.plugin
class Yakafokon:
    """ YKFK plugin """
    def __init__(self, bot):
        self.bot = bot
        self.log = self.bot.log

    @irc3.event(irc3.rfc.PRIVMSG)
    def ykfk(self, mask, event, target, data):
        yakafokon = ['falloir', 'faut', 'il faille', 'faudra', 'fallait', 'il fallût', 'fallu']
        if [terme for terme in yakafokon if terme in data]:
            self.bot.privmsg(target, "¡¡¡ YAKAFOKON detected !!!")
