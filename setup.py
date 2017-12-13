#!/usr/bin/env python

"""
This module implements a set of requests TransportAdapter, PoolManager,
ConnectionPool and HTTPSConnection with one goal only:

to use a specific IP address when connecting via SSL to a web service without
running into SNI trouble.  The usual technique to force an IP address on an
HTTP connection with Requests is (assuming I want http://example.com/some/path
on IP 1.2.3.4):

requests.get("http://1.2.3.4/some/path", headers={'Host': 'example.com'})

this is useful if I want to specifically test how 1.2.3.4 is responding;
for instance, if example.com is DNS round-robined to several IP addresses
and I want to hit one of them specifically.
"""
from setuptools import setup, find_packages


PACKAGE_NAME = 'forcediphttpsadapter'
PACKAGE_VERSION = '1.0.0'
AUTHOR = 'Roadmaster'
EMAIL = 'daniel@tomechangosubanana.com'
URL = 'https://github.com/Roadmaster/forcediphttpsadapter'


setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    description=__doc__,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    # classifiers=CLASSIFIERS,
    # platforms=PLATFORMS,
    provides=['adapters'],
    install_requires=['requests'],
    # dependency_links=dependency_links,

    packages=find_packages(),
    # include_package_data=True,
    # package_data=package_data,

    download_url='{}/archive/master.zip'.format(URL),
    # keywords=KEYWORDS,
    # scripts=scripts,

    # entry_points={},

    zip_safe=False,
)
