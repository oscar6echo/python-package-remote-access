
# Python Package Remote Access - Server

## 1 - Installation

Download the folder **/server** from this repo:
```bash
mkdir client && cd client && curl https://codeload.github.com/oscar6echo/python-package-remote-access/tar.gz/master | tar -xz --strip=2 python-package-remote-access-master/server
```

## 2 - User Guide

+ Copy/paste your Python package(s) folder(s) in this folder **/server** next to **/server/app.py**.  
+ Add the package(s) name(s) to file **/api/swagger/packages.txt**.  
+ Restart the server.  
+ Then clients can access your package(s) classes and functions, using the corresponding [client package](../client).  

## 1 - Limitations

Classes and functions in your package(s) **must return pickle-able** objects.  
Essentially these are all Python objects but user defined objects or functions.  
Example of supported formats:
+ Python types (int, float, str, list, tuple, dict, datetime)
+ numpy (ndarray)
+ pandas (Timestamp, DataFrame, Series)

Also note that **local print() is not visible** from remote. Only returned values are.

## 4 - Endpoints

Open the swagger screen at http://[ip]:[port]/[version]/ui.  
Example: http://localhost:9090/v1.0/ui/

+ **/info** returns the structure of the package(s) served.
+ **/exec** is the action endpoint used by the client to:
    + launch a remote function
    + instantiate a remote class
    + launch a remote method
