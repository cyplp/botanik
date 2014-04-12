import sqlite3
from os.path import exists, dirname, expanduser
import re
from urllib.parse import urlparse
from os import makedirs

import irc3
from irc3.plugins.command import command
import requests
from bs4 import BeautifulSoup


@irc3.plugin
class Urls:
    """
    A plugin for print Url title
    """
    def __init__(self, bot):
        self.bot = bot
        self.log = self.bot.log

        if 'paulla.ircbot.plugins.Urls' in self.bot.config\
                and 'db' in self.bot.config['paulla.ircbot.plugins.Urls']\
                and self.bot.config['paulla.ircbot.plugins.Urls']['db']:
            db = self.bot.config['paulla.ircbot.plugins.Urls']['db']
        else:
            db = '~/.irc3/Urls.db'
        if '~' in db:
            db = expanduser(db)
        if not exists(db):
            if not exists(dirname(db)):
                makedirs(dirname(db))
            open(db, 'a').close()
        self.conn = sqlite3.connect(db)
        cur = self.conn.cursor()
        cur.execute('''create table if not exists url
                (id_url integer primary key,
                value text,
                title text,
                dt_inserted datetime,
                nick text
                )''')
        cur.execute('''create table if not exists tag
                (id_tag integer primary key,
                id_url interger,
                value text
                dt_inserted datetime,
                nick text
                )''')

        cur.execute('''create table if not exists old
                (id_old integer primary key,
                value text,
                dt_inserted datetime,
                nick text
                )''')
        self.conn.commit()
        cur.close()


    @irc3.event(irc3.rfc.PRIVMSG)
    def url(self, mask, event, target, data):
        """
        parse and reply url title
        """
        urls = re.findall('(?P<url>http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)', data)

        nick = mask.split('!')[0]

        for url in urls:
            req = requests.get(url)
            soup = BeautifulSoup(req.content)
            title = soup.title.string.encode('ascii', 'ignore').decode('ascii', 'ignore')
            domain = urlparse(url).netloc.split(':')[0]
            self.bot.privmsg(target, "Title: %s - (at %s)" % (title, domain))

            cur = self.conn.cursor()

            cur.execute("SELECT dt_inserted, nick from url where value='%s'" % url)
            data = cur.fetchall()

            if data:
                self.displayOld(target, nick, data[0][0])
            else:
                cur.execute("INSERT INTO url(value, title, nick, dt_inserted) VALUES('%s', '%s', '%s', datetime('now')) ;" % (url, title, nick))
                self.conn.commit()
            cur.close()

    def displayOld(self, target, nick, dt_inserted):
        cur = self.conn.cursor()
        cur.execute("SELECT value FROM old ORDER BY RANDOM() LIMIT 1")
        data = cur.fetchall()
        if data:
            self.bot.privmsg(target, '%s %s %s' % (nick, data[0][0], dt_inserted))
        cur.close()

    @command
    def old(self, mask, target, args):
        """old command

           %%old <add/remove> <message>...
        """
        nick = mask.split('!')[0]

        if args['<add/remove>'].lower() == 'add':
            cur = self.conn.cursor()
            cur.execute("INSERT INTO old(value, nick, dt_inserted) VALUES('%s', '%s', datetime('now'));" %(str(' '.join(args['<message>'])).replace("'", "''"), nick))
            self.conn.commit()
            return

        if args['<add/remove>'].lower() == 'remove':
            cur = self.conn.cursor()
            cur.execute("DELETE FROM old where value= '%s';" %(str(' '.join(args['<message>'])).replace("'", "''") ))
            self.conn.commit()
            return


# end of file
