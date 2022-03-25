import random
import re
import time
import unittest

from util import hook



def get_quotes_by_string(db, msg):
    return db.execute("select time, nick, msg from quote where deleted!=1 "
                      "and chan='#phiz' and msg like ? order by time",
                      (msg,)).fetchall()


#def get_quotes_by_chan(db, chan):
 #   return db.execute("select time, nick, msg from quote where deleted!=1 "
  #                    "and chan=? order by time", (chan,)).fetchall()

#def get_quote_by_id(db, num):
 #   return db.execute("select time, nick, msg from quote where deleted!=1 "
  #                    "and rowid=?", (num,)).fetchall()


def format_quote(q, num, n_quotes):
    ctime, nick, msg = q
    return "[%d/%d] %s <%s> %s" % (num, n_quotes,
                                   time.strftime("%Y-%m-%d", time.gmtime(ctime)), nick, msg)


@hook.command('qsearch')
@hook.command
def quotesearch(inp, nick='', chan='', db=None, admin=False):
    ".qsearch/.quotesearch <string> " \
        "im working on it bitch, " \
        " also i'm no longer gay"



#    search = re.match(r"(search \S+)\s+(\S+)(?:\s+#?(-?\d+))?$", inp)
#    add = re.match(r"add[^\w@]+(\S+?)>?\s+(.*)", inp, re.I)
#    delete = re.match(r"delete[^\w@]+(\S+?)>?\s+(.*)", inp, re.I)
#    retrieve_search = re.match(r"search[^\w@]+(\S+?)>?\s+(.*)", inp, re.I)
    retrieve = re.search(r"(\S+)(?:\s+#?(-?\d+))?$", inp)
#    retrieve_chan = re.match(r"(#\S+)\s+(\S+)(?:\s+#?(-?\d+))?$", inp)
#    retrieve_id = re.match(r"(\d+)$", inp)
  
    if retrieve:
        chan = '#phiz'
        msg = "%" +inp + "%"
        #select, msg = retrieve.groups()
        quotes = get_quotes_by_string(db, msg)

    else:
        return quotesearch.__doc__


    #if num:
    #   num = int(num)

    n_quotes = len(quotes)

    if not n_quotes:
        return "no quotes found for ' " + msg + " ' "
    else:
        num = random.randint(1, n_quotes)
        selected_quote = quotes[num - 1]

    #if num:
    #    if num > n_quotes or (num < 0 and num < -n_quotes):
    #        return "I only have %d quote%s for %s" % (n_quotes,
    #                                                  ('s', '')[n_quotes == 1], select)
    #    elif num < 0:
    #        selected_quote = quotes[num]
    #        num = n_quotes + num + 1
    #    else:
    #        selected_quote = quotes[num - 1]

    return format_quote(selected_quote, num, n_quotes)


class QuoteTest(unittest.TestCase):
    def setUp(self):
        import sqlite3
        self.db = sqlite3.connect(':memory:')

        quote('', db=self.db)  # init DB

    def quote(self, arg, **kwargs):
        return quote(arg, chan='#test', nick='alice', db=self.db, **kwargs)

    def add_quote(self, msg=''):
        add_quote(self.db, '#test', 'Socrates', 'Plato',
                  msg or 'Education is the kindling of a flame,'
                  ' not the filling of a vessel.')

    def test_retrieve_chan(self):
        self.add_quote()
        assert '<Socrates> Education' in self.quote('#test')

    def test_retrieve_user(self):
        self.add_quote()
        assert '<Socrates> Education' in self.quote('socrates')

    def test_no_quotes(self):
        assert "no quotes found" in self.quote("#notachan")

    def test_quote_too_high(self):
        self.add_quote()
        assert 'I only have 1 quote for #test' in self.quote('#test 4')

    def test_add(self):
        self.quote("add <someone> witty phrase")
        assert 'witty' in self.quote('#test')

    def test_add_twice(self):
        self.quote("add <someone> lol")
        assert 'already stored' in self.quote("add <someone> lol")

    def test_del_not_admin(self):
        assert 'only admins' in self.quote('delete whoever 4')

    def test_del_not_exists(self):
        assert 'found no matching' in self.quote(
            'delete whoever 4', admin=True)

    def test_del(self):
        self.add_quote("hi")
        assert "deleted quote 'hi'" in self.quote(
            'delete socrates hi', admin=True)

    def test_retrieve_id(self):
        self.add_quote()
        assert 'Education is' in self.quote('1')

    def test_retrieve_chan_user(self):
        self.add_quote()
        assert 'Education' in self.quote('#test socrates')
        assert 'Education' in self.quote('#test socrates 1')

    def test_nth(self):
        self.add_quote('first quote')
        self.add_quote('second quote')
        self.add_quote('third quote')
        self.add_quote('fourth quote')
        assert 'third' in self.quote('socrates -2')
        assert 'only have 4' in self.quote('socrates -9')

if __name__ == '__main__':
    unittest.main()
