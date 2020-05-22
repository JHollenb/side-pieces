# Level 2
1. Create a TCP server communications interface program that meets the following requirements:
    a. Accepts and processes one connection at a time
    b. Processes requests from the client and provides responses
    c. Logs the interaction
2. How would you add privacy to the communications?
3. How would you add authentication to the communications?

# Design
## TCP/IP
First, lets go over TCP/IP. TCP/IP is simply a system of protocols used to securely transfer data.

A TCP/IP system must do the following:

* breakup messages into manageable chunks for all layers;
* Interface with network adapters;
* Recognize addressing;
* Route data to the proper network and subnet;
* Error control;
* Forward local data to network;
* Receive data from network and pass to local systems.

To do the aforementioned task, TCP/IP breaks itself up into a few layers. They are as follows:
```
--------------------
Application Layer
--------------------
Transport Layer
--------------------
Internet Layer
--------------------
Network Access Layer
--------------------
```

* Network Access Layer - Interface with physical network. Formats data for transmission medium and addresses data for the subnet based on physical hardwar addresses. Provide error control for data delivered on the physical network.
* Internet Layer - Provides logical, hardware-independent addressing (IP addresses)
* Transport Layer - Flow-control, error-control, and acknowledgement services for the internetwork. Serves the interfacefor network applications.
* Application Layer - Provides applications for troubleshooting, file transfer, remote control, and Internet activities.

We might be getting into the weeds here. All of the stuff is handled with our python library. I 
will leave it there because I spent a bit of time researching it. 

### Server
Basically we want to create a server that will do the following:
1. Create a socket object (IPV4)
1. Bind an address and port to socket
1. Listen for connections
1. Accept incoming connections
1. Try to recieve data

### Client
1. Create a socket object (IPV4)
1. Try to connect to socket using an address and port
1. Send our data
1. Profit!

# Privacy
Now to address privacy. Python has a library called `ssl`. This library has some functionality 
that we may find interesting for this project. From the python docs for [ssl](https://docs.python.org/3/library/ssl.html):
> This module provides access to Transport Layer Security (often known as “Secure Sockets Layer”) 
> encryption and peer authentication facilities for network sockets, both client-side and 
> server-side. This module uses the OpenSSL library. It is available on all modern Unix systems, 
> Windows, Mac OS X, and probably additional platforms, as long as OpenSSL is installed on that 
> platform.

Sounds pretty cool.

# Authentication
Encrypt using AES
Public/Private key


