# -*- coding: utf-8 -*-

import socket
HOST = '192.168.1.12'
PORT = 8005
THIS_PORT = 8002
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, THIS_PORT))
s.connect((HOST, PORT))
data = bytes("GET / HTTP/1.0\n\n", 'utf-8') #python3 has a new "bytes" data type
s.send(data)
data = str(s.recv(1000), 'utf-8')

print("CLIENT: Recieved {} bytes:\n=====\n{}\n=====".format(len(data), data))
