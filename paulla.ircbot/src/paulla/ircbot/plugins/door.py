import irc3
from irc3.plugins.cron import cron
import requests
from datetime import datetime


@irc3.plugin
class Door:
    """
    Door state plugin
    """

    def __init__(self, bot):
        self.bot = bot
        self.log = self.bot.log

    @irc3.event(irc3.rfc.MY_PRIVMSG)
    def question(self, mask, event, target, nick, data):
        #TODO
        pass

    @irc3.event(irc3.rfc.PRIVMSG)
    def question(self, mask, event, target, data):
        #TODO
        pass

    @cron('*/1 * * * *')
    def anoncement(self):
        r = requests.get('http://sd-36895.dedibox.fr:2222').json()
        last_change = datetime.strptime(r['lastchange'], "%d/%m/%Y %H:%M:%S")
        if (datetime.now() - last_change).seconds < 60:
            if "0" in r['state']:
                self.bot.privmsg('#test-mika','Le lab est ouvert')
            elif "1" in r['state']:
                self.bot.privmsg('#test-mika','Le lab viens de fermer')
        
