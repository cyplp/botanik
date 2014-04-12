import irc3
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse


@irc3.plugin
class Urls:
    """
    A plugin for print Url title
    """
    def __init__(self, bot):
        self.bot = bot
        self.log = self.bot.log

    @irc3.event(irc3.rfc.PRIVMSG)
    def url(self, mask, event, target, data):
        """
        parse and reply url title
        """
        bot = self.bot
        urls = re.findall('(?P<url>http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)', data)
        for url in urls:
            r = requests.get(url)
            soup = BeautifulSoup(r.content)
            title = soup.title.string.encode('ascii', 'ignore').decode('ascii', 'ignore')
            domain = urlparse(url).netloc.split(':')[0]
            self.bot.privmsg(target, "Title: %s - (at %s)" % (title, domain))
# end of file
