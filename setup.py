#!/usr/bin/env python

"""
This module implements a set of requests TransportAdapter, PoolManager,
ConnectionPool and HTTPSConnection allowing use of a specific IP address when
connecting via SSL to a web service without running into SNI trouble.
"""
from setuptools import setup, find_packages


PACKAGE_NAME = "forcediphttpsadapter"
PACKAGE_VERSION = "1.0.2"
AUTHOR = "Roadmaster"
EMAIL = "daniel@tomechangosubanana.com"
URL = "https://github.com/Roadmaster/forcediphttpsadapter"


setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    description=__doc__.replace("\n", " "),
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    # classifiers=CLASSIFIERS,
    # platforms=PLATFORMS,
    provides=["adapters"],
    install_requires=["packaging", "requests"],
    # dependency_links=dependency_links,
    packages=find_packages(),
    # include_package_data=True,
    # package_data=package_data,
    download_url="{}/archive/master.zip".format(URL),
    # keywords=KEYWORDS,
    # scripts=scripts,
    # entry_points={},
    zip_safe=False,
)
