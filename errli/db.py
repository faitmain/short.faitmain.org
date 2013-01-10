""" Database
"""
import binascii
import os
import urllib2

from BeautifulSoup import BeautifulSoup
from sqlalchemy import create_engine, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Text
from sqlalchemy.sql import text


_Base = declarative_base()


class Short(_Base):
    __tablename__ = 'short'
    id = Column(Integer, primary_key=True)
    short_url = Column(String(100), nullable=False)
    long_url = Column(Text(), nullable=False)
    hits = Column(Integer, default=0)


short = Short.__table__


GET_LONG = text("""\
select
    long_url
from
    short
where
    short_url = :short_url
""")


GET_SHORT = text("""\
select
    short_url
from
    short
where
    long_url = :long_url
""")


ADD = text("""\
insert into short
    (long_url, short_url)
values
    (:long_url, :short_url)
""")


HIT = text("""\
update
    short
set
    hits = hits + 1
where
    short_url = :short_url
""")


def _random(url):
    return binascii.b2a_hex(os.urandom(4))[:4]


def _smart(url, tries):
    # let's get the content of the page
    soup = BeautifulSoup(urllib2.urlopen(url))

    # we want to build a short with the page title
    if soup.title is None:
        return _random(url)

    title = soup.title.string

    words = [word.lower() for word in
                 [word.strip() for word in title.split()]
             if len(word) > 4 and word[0] != '&']

    # that works for Sphinx :)
    short = words[0] + '-' + words[1]
    if tries > 0:
        short += '-' + str(tries)

    return short


class SQLStorage(object):

    def __init__(self, sqluri, shortener=_smart):
        self.engine = create_engine(sqluri)
        short.metadata.bind = self.engine
        short.create(checkfirst=True)
        self.shortener = shortener

    def add_short_url(self, long_url):
        short = self.get_short_url(long_url)
        if short is not None:
            return short

        new_short = None
        tries = 0

        while new_short is None and tries < 100:
            short = self.shortener(long_url, tries)

            if self.get_long_url(short) is None:
                new_short = short
            else:
                tries += 1

        if new_short is None:
            raise ValueError("Cannot do this")

        self.engine.execute(ADD, short_url=new_short, long_url=long_url)
        return new_short

    def get_long_url(self, short_url, hit=True):
        res = self.engine.execute(GET_LONG, short_url=short_url)
        res = res.fetchone()
        if res is None:
            return None
        if hit:
            # let's increment the hit
            self.engine.execute(HIT, short_url=short_url)
        return res.long_url

    def get_short_url(self, long_url):
        res = self.engine.execute(GET_SHORT, long_url=long_url)
        res = res.fetchone()
        if res is None:
            return None
        return res.short_url
