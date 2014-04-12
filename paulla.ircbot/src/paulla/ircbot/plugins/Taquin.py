import irc3
from irc3.plugins.command import command
import sqlite3
from os.path import exists, dirname, expanduser
from os import makedirs
from random import sample


@irc3.plugin
class Taquin:
    """A plugin for joke
    """
    def __init__(self, bot):
        self.bot = bot
        self.log = self.bot.log
        if 'paulla.ircbot.plugins.Taquin' in self.bot.config\
                and 'db' in self.bot.config['paulla.ircbot.plugins.Taquin']\
                and self.bot.config['paulla.ircbot.plugins.Taquin']['db']:
            db = self.bot.config['paulla.ircbot.plugins.Taquin']['db']
        else:
            db = '~/.irc3/taquin.db'
        if '~' in db:
            db = expanduser(db)
        if not exists(db):
            if not exists(dirname(db)):
                makedirs(dirname(db))
            open(db, 'a').close()
        self.conn = sqlite3.connect(db)
        cur = self.conn.cursor()
        cur.execute('''create table if not exists Taquin
                (id integer primary key,
                nick text,
                keyword text,
                message text
                )''')
        self.conn.commit()
        cur.close()

    @irc3.event(irc3.rfc.PRIVMSG)
    def taquin_say(self, mask, event, target, data):
        if event == 'PRIVMSG' \
                and not data.startswith('!')\
                and mask.nick != self.bot.nick:
            cur = self.conn.cursor()
            words = [word for word in data.split() if word.isalnum()]
            for word in words:
                cur.execute("""
                select message from Taquin where keyword = '%s'
                """ % word)
                result = cur.fetchall()
                if result:
                    message = sample(result, 1)[0][0]
                    self.bot.privmsg(target, message)
            cur.close()

    @command
    def taquin(self, mask, target, args):
        """Echo command

           %%taquin <add/remove> <nick> <keyword> <message>...
        """
        if args['<add/remove>'].lower() == 'add':
            cur = self.conn.cursor()
            cur.execute("insert into Taquin(nick, keyword, message) values ('%s','%s','%s')" %
                    (
                        args['<nick>'],
                        args['<keyword>'],
                        ' '.join(args['<message>']),
                        )
                    )
            self.conn.commit()
            cur.close()
        elif args['<add/remove>'].lower() == 'remove':
            cur = self.conn.cursor()
            cur.execute("select * from Taquin where nick = '%s' and keyword = '%s'" %
                    (
                        args['<nick>'],
                        args['<keyword>'],
                        )
                    )
            if cur.fetchone():
                cur.execute("delete from Taquin where nick = '%s' and keyword = '%s'" %
                        (
                            args['<nick>'],
                            args['<keyword>'],
                            )
                        )
            else:
                self.bot.privmsg(target, mask.nick + ' : nick/keyword not match')
            self.conn.commit()
            cur.close()
        else:
            self.bot.privmsg(mask.nick, 'Invalid arguments')
