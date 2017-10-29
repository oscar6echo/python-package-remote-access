# Python Package Remote Access

## 1 - Summary

+ **Serve any Python package over to remote clients without writing any server code and creating specific endpoints.**  
+ Additionally the served packages can be navigated interactively in a Juptyer notebook.  
+ The only constraint is that results from package classes and functions must be pickle-able - and the server and client must have the same pickle version.

## 2 - Principles

List all packages to be served in file **/server/api/swagger/packages.txt** and place the corresponding packages in folder **/server**.  
At startup the server creates a json representation of the packages listed in file .  
Such representation contains the tree of files in each package and for each file the functions and classes in it.  
For each function and class method, the arguments and their default value are recorded.  
See this file **[/server/struct.json]()** for an example.  

This information is sent to the clients upon connection.  
From it a client can construct a "shallow" package that will call the server for any code execution - function, class instance creation, and instance method execution.  

The mechanism broadly described above uses only 2 server endpoints - independent of the packages served:
+ **/info**: returns the json representation of packages served
+ **/exec**: returns the result of any code execution - functions, class instance creation, instance method execution

Under the hood the client constructs:
+ a lambda function for each remote variable - to read it on the server.
+ a lambda function for each remote function - to request its execution by the server.
+ a lambda function for each remote class - to request an instance creation by the server.

When a client launch the creation of an instance of a remote class, then all its methods are constructed in the same way.

To keep the state of an instances from its creation to the next method execution and so on, the client uses a global store.

## 3 - Use cases

You may ask: Why all this ? Is it not simpler to just put a package on pypi ?  
Ok it requires some work. Additionally if your package has dependencies not broadly available it is better to serve it.  
But if you do then you usually have to define and maintain and document endpoints and the plumbing code to your package functions and classes.  
Now if you are in a fast moving environnemnt where:
+ your package must evolve quickly
+ your clients have personal workflows and do a lot of prototyping

this is cumbersome and it takes some extra skills to do that properly.  

Well this repo aims at addressing this situation exactly.  
It will suit a small to medium sized team in a corporation for example.  
It may have other use cases beyond that too.. 

## 4 - User Guide

### 4.1 - Server

Read [here](server/README.md).

### 4.2 - Client

Read [here](client/README.md).

### 4.3 - Name Server

This is not absolutely necessary but included as a convenient service.  
Your clients need only know the nameserver url to located and connect to your server.  
Read [here](nameserver/README.md).


## 5 - Origin

This repo is inspired by this [Python-object-over-API repo](https://github.com/PierreMarion23/Python-object-over-API) and the result of continued interaction with its author.  
If you have ideas about how to widen its scope of make its implementation more robust please **do get in touch !**  
