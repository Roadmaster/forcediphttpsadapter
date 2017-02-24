#!/usr/bin/env python2
import argparse
import logging
import requests
import sys
import urlparse


# If the adapter import fails, set it to None
# so we know we can't really use it.
try:
    from adapters import ForcedIPHTTPSAdapter
except ImportError:
    ForcedIPHTTPSAdapter = None

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument("url")
parser.add_argument(
    "--forced-ip",
    help="IP to use, instead of the one the URL resolves to.")
args = parser.parse_args()

uri = args.url
ip = args.forced_ip
print(args)
url_parts = urlparse.urlsplit(uri)
hostname = url_parts.netloc
session = requests.Session()

if ForcedIPHTTPSAdapter and url_parts.scheme == "https":
    # Adapter is available, use it regardless of Python version
    base_url = urlparse.urlunsplit((
        url_parts.scheme, url_parts.netloc, "", "", ""))
    session.mount(base_url, ForcedIPHTTPSAdapter(dest_ip=ip))
else:
    # Fall back to old hack-ip-into-url behavior, for either
    # https with no adapter, or http.
    if ip:
        url_parts = url_parts._replace(netloc=ip)
        uri = urlparse.urlunsplit(url_parts)
if (not ForcedIPHTTPSAdapter and
    url_parts.scheme == "https" and
        sys.version_info >= (2, 7, 9)):
    # Just a message so 400 errors don't come as a surprise.
    logging.error(
        "Can't reliably force IP with this combination of "
        "Python/Requests. This check is likely to return "
        "a 400 Bad Request code.")

log.info("Testing %s with hostname %s (forced IP: %s)",
         uri, hostname, ip)

response = session.get(uri, headers={'Host': hostname}, verify=False)
print(response)
