import json
from random import randint
# import socket
# import multiprocessing
# import argparse

nodes = {0: ("192.168.1.12", 8006),
         1: ("192.168.1.12", 8002),
         2: ("192.168.1.12", 8010),
        #  3: ("192.168.1.17", 5005),
         }
# nodes.pop(nodes[socket.get]) #zastanowic sie czy warto usuwac biezacy node z listy nodes powyzej
# czy to czasami nie wymaga zmodyfikowania prep_trajectory zeby bralo jedynie elementy z nodes.keys

N = len(nodes)
n = 3
ACKNOWLEDGED = "HADHGFHGFHSETYRSHTDHGSUDGHGUHSEYGHERGAHGEAT"

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
def receive(s):
    connection, address = s.accept()
    print("Accepted connection from {}".format(address))
    print(5*"=")
    encoded_list = ""
    while 1:
        data = connection.recv(1000)
        if not data: break
        received_data_part = str(data, 'utf-8')
        print(received_data_part)
        encoded_list = encoded_list + received_data_part
        connection.sendall(data)
    connection.close()
    print(5*"=")
    origin_ip = address #from socket
    return encoded_list, origin_ip
