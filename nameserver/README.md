
# Python Package Remote Access - Nameserver

## 1 - Installation

Download the folder **/nameserver** from this repo:
```bash
mkdir client && cd client && curl https://codeload.github.com/oscar6echo/python-package-remote-access/tar.gz/master | tar -xz --strip=2 python-package-remote-access-master/nameserver
```
## 2 - User Guide

+ Write all servers info in file `api/swagger/servers.txt`.  
    On each line "[name of server], [ip address], [port], [version]"  
    For example "myserver,  localhost, 9090, v1.0"
+ Restart the server

## 3 - Endpoints

Open the swagger screen at http://[ip]:[port]/[version]/ui.  
Example: http://localhost:9999/v1.0/ui/

+ `/info` returns a dictionary of servers  
    For example {'myserver': {'ip': 'localhost', 'port': '9090', 'version': 'v1.0'}}
