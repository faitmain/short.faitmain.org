"""Main entry point
"""
from pyramid.config import Configurator
from errli.db import SQLStorage


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include("cornice")
    config.scan("errli.views")
    config.registry['storage'] = SQLStorage(settings['sqluri'])
    return config.make_wsgi_app()
