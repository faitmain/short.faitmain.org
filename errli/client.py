""" Client lib
"""
import urllib2
import json
import sys


_SERVER = 'http://short.faitmain.org'
_KEY = 'booba81'


def shorten(url):
    req = urllib2.Request(_SERVER, headers={'X-Short': _KEY})
    req.get_method = lambda: 'POST'
    req.add_data(url)
    res = urllib2.urlopen(req).read()
    res = json.loads(res)
    return _SERVER + '/' + res['short']


def main():
    print shorten(sys.argv[1])


if __name__ == '__main__':
    main()


