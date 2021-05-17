This module implements a set of requests TransportAdapter, PoolManager,
ConnectionPool and HTTPSConnection with one goal only:

* to use a specific IP address when connecting via SSL to a web service without
running into SNI trouble.

The usual technique to force an IP address on an HTTP connection with Requests
is (assuming I want http://example.com/some/path on IP 1.2.3.4):

```
requests.get("http://1.2.3.4/some/path", headers={'Host': 'example.com'})
```

this is useful if I want to specifically test how 1.2.3.4 is responding; for
instance, if example.com is DNS round-robined to several IP
addresses and I want to hit one of them specifically.

This also works for https requests if using Python <2.7.9 because older
versions don't do SNI and thus don't pass the requested hostname as part of the
SSL handshake.

However, Python >=2.7.9 and >=3.4.x conveniently added SNI support, breaking
this way of connecting to the IP, because the IP address embedded in the URL
*is* passed as part of the SSL handshake, causing errors (mainly, the server
returns a 400 Bad Request because the SNI host 1.2.3.4 doesn't match the one in
the HTTP headers example.com).

The "easiest" way to achieve this is to force the IP address at the lowest
possible level, namely when we do socket.create_connection. The rest of the
"stack" is given the actual hostname. So the sequence is:

1. Open a socket to 1.2.3.4
2. SSL wrap this socket using the hostname.
3. Do the rest of the HTTPS traffic, headers and all over this socket.

Unfortunately Requests hides the socket.create_connection call in the deep
recesses of urllib3, so the specified chain of classes is needed to propagate
the given dest_ip value all the way down the stack.

Because this applies to a very limited set of circumstances, the overridden
code is very simplistic and eschews many of the nice checks Requests does for
you.

Specifically:

- It ONLY handles HTTPS.
- It does NO certificate verification (which would be pointless)
- Only tested with Requests 2.2.1 and 2.9.1.
- Does NOT work with the ancient urllib3 (1.7.1) shipped with Ubuntu 14.04.
  Should not be an issue because Ubunt 14.04 has older Python which doesn't do
  SNI.


How to use it
=============

First install it:

```
pip install forcediphttpsadapter
```

Then, it's like any other transport adapter. Just pass the IP address that
connections to the given URL prefix should use.

```
from forcediphttpsadapter.adapters import ForcedIPHTTPSAdapter

session = requests.Session()
session.mount("https://example.com", ForcedIPHTTPSAdapter(dest_ip='1.2.3.4'))
response = session.get(
    '/some/path', headers={'Host': 'example.com'}, verify=False)
```

Note this module will ImportError if there's no sane requests/urllib
combination available so the adapter won't work, and it's up to the caller to
decide what to do. The caller can, for instance, check the Python version and
if it's &lt;2.7.9 decide to use the old "http://$IP/ technique. If Python is
&gt;=2.7.9 and the adapter doesn't work, unfortunately, there's nothing that can
be done :(

An example.py script is provided, it illustrates how to
import the module, how to decide whether to use the adapter
or the old technique, and how to define the IP and mount
the adapter on a session.
