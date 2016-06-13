import json
from random import randint
# import socket
# import multiprocessing
# import argparse

nodes = {0: ("192.168.0.11", 8006),
         1: ("192.168.0.11", 8002),
         2: ("192.168.0.11", 8010),
        #  3: ("192.168.1.17", 5005),
         }
# nodes.pop(nodes[socket.get]) #zastanowic sie czy warto usuwac biezacy node z listy nodes powyzej
# czy to czasami nie wymaga zmodyfikowania prep_trajectory zeby bralo jedynie elementy z nodes.keys

N = len(nodes)
n = 3
ACKNOWLEDGED = "HADHGFHGFHSETYRSHTDHGSUDGHGUHSEYGHERGAHGEAT"
add_client = "ADD_CLIENT"

def prep_trajectory(n):
    """return trajectory as randomized ordered list of nodes to be traversed in TOR packet cycle.
    nodes do not lead directly to the same node

    n: length of trajectory
    """
    trajectory = [randint(0,N-1) for i in range(n)]
    for i in range(n):
        while trajectory[i] == trajectory[i-1]:
            trajectory[i] = randint(0,N-1)
    return trajectory

def encode_trajectory(trajectory, message, target, sender):
    """ takes trajectory list (use prep_trajectory) and string message

    returns trajectory and message as nested list in JSON string form
    """
    lista = [target, message] #OSTATNI MUSI ZAWIERAĆ ADRES DOCELOWEGO ODBIORCY
    n = len(trajectory)
    for i in range(n):
        lista = [trajectory[n-1-i], lista]
    return json.dumps(lista)

def send(ip, string_message):
    """TODO: socket"""
    pass

def receive(connection, address):
    print("Accepted connection from {}".format(address))
    print(5*"=")
    received_data = ""
    while 1:
        data = connection.recv(1000)
        if not data: break
        received_data_part = str(data, 'utf-8')
        received_data = received_data + received_data_part
        connection.sendall(data)
    connection.close()
    print(received_data)
    print(5*"=")
    origin_ip = address #from socket
    return received_data, origin_ip
