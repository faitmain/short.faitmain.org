""" Setup file.
"""
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()


setup(name='errli',
    version=0.1,
    description="Url shortener",
    long_description=README,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "License :: OSI Approved :: Apache Software License"],
    keywords="web services",
    author='Tarek Ziade',
    author_email="Tarek Ziade -at- example.com",
    url="http://example.com",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['cornice', 'PasteScript', 'WebTest', 'SQLAlchemy',
                      'BeautifulSoup', 'unidecode'],
    entry_points="""\
    [paste.app_factory]
    main = errli:main

    [console_scripts]
    errli = errli.client:main

    """,
    paster_plugins=['pyramid'],
)
