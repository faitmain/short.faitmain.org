""" Cornice services.
"""
from cornice import Service
from webob import exc


redirect = Service(name='redirect', path='/{short_url}',
                   description="Redirect")
short = Service(name='shortener', path='/', description="URL Shortener")


def get_storage(request):
    return request.registry['storage']


def auth(request):
    """Look for an authorized key.
    """
    key = request.headers.get('X-Short')
    if key is None or not key in request.registry.settings['keys']:
        raise exc.HTTPUnauthorized()


@short.post(validators=(auth,))
def new_url(request):
    """Adds a shortened URL."""
    url = request.body
    if url == '':
        raise exc.HTTPBadRequest()

    short = get_storage(request).add_short_url(url)
    return {'short': short}


@short.get(renderer='string')
def home(request):
    return 'Welcome to err.li'


@redirect.get()
def get_url(request):
    """Adds a shortened URL."""
    short_url = request.matchdict['short_url']
    long_url = get_storage(request).get_long_url(short_url)
    if long_url is None:
        request.matchdict = None  # XXX o/wise cornice throws a 405
        raise exc.HTTPNotFound()

    return exc.HTTPFound(location=long_url)


@redirect.delete(validators=(auth,))
def delete_url(request):
    """Removes a shortened URL."""
    raise NotImplementedError()
