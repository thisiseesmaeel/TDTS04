from socket import *
import re


serverName = "zebroid.ida.liu.se"
serverPort = 80
request = """GET /fakenews/test1.txt HTTP/1.1
Host: zebroid.ida.liu.se
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
Upgrade-Insecure-Requests: 1

"""

content = """HTTP/1.1 200 OK
Date: Sat, 06 Feb 2021 09:44:51 GMT
Server: Apache/2.4.6 (CentOS) mod_auth_gssapi/1.5.1 mod_nss/1.0.14 NSS/3.28.4 mod_wsgi/3.4 Python/2.7.5
Last-Modified: Fri, 15 Jan 2021 11:35:41 GMT
ETag: "17f-5b8eec5af0616"
Accept-Ranges: bytes
Content-Length: 383
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Content-Type: text/plain; charset=UTF-8

This is a basic text file.
It tells a simple story about our yellow friend Smiley,
who is from Stockholm. Smiley is round, I think.

Without your proxy, you should be able to view this page just fine.

With your proxy, this page should look a bit different,
with all mentions of Smiley from Stockholm
being changed into something else.  
The page should still be formatted properly."""

altered_content = re.sub("Smiley", "Trolly", content)
print("Orginal content:\n{}\nAltered content:\n{}".format(content, altered_content))

