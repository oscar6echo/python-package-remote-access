
# Python Package Remote Access - Client

## 1 - Installation

### 1.1 - Manual
Download the folder **/client** from this repo:
```bash
mkdir client && cd client && curl https://codeload.github.com/oscar6echo/python-package-remote-access/tar.gz/master | tar -xz --strip=2 python-package-remote-access-master/client
```

### 1.2 - pip
Or install via pip (TBD):
```bash
pip install remote-access-client
```

## 2 - User Guide

+ Import client

```python
# manual
import client as prc
# pip
import package_remote_access.client as prc
```

+ Connect to server by url

```python
rc = prc.Connect(url_server='http://localhost:9090/v1.0')
```

+ Or connect to server by name

```python
rc = prc.Connect(url_nameserver='http://localhost:9999/v1.0',
                 server_name='myserver')
```

+ Checkout the remote packages structure

```python
rc.struct
```

+ Get a handle of the remote packages

```python
handle = rc.build_remote_package()
```

From there work as usual

+ Execute function

```python
m = handle.sample_package_B.file1
m.hello(1, 2, 3, **{'abc': 'azerty'})
```
+ Instantiate class

```python
m = handle.sample_package_B.file1
m.hello(1, 2, 3, **{'abc': 'azerty'})
```

+ Execute instance method

```python
a.polite('Auguste')
```
+ Get variable value

```python
# Exception: remote variable are made functions so add ()
f.TATA()
```


## 3 - Notebooks

For more info read and compare the demo
+ [local-access notebook](../server/local-access.ipynb)
+ [remote-access notebook](../remote-access.ipynb)
