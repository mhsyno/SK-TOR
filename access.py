import json
from random import randint
import socket
import multiprocessing
import argparse

parser = argparse.ArgumentParser(description='Lorem ipsum!')
parser.add_argument('current_node_ID', type=int, nargs='+',
                    help="this node's ID")
args = parser.parse_args()
current_node_ID,  = args.current_node_ID


nodes = {0: ("192.168.1.12", 8005),
         1: ("192.168.1.17", 5005),
         2: ("192.168.1.12", 8002),
         }
# nodes.pop(nodes[socket.get]) #zastanowic sie czy warto usuwac biezacy node z listy nodes powyzej
# czy to czasami nie wymaga zmodyfikowania prep_trajectory zeby bralo jedynie elementy z nodes.keys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(nodes[current_node_ID])
print("Listening on {}".format(nodes[current_node_ID]))

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
    lista = [sender, message] #OSTATNI MUSI ZAWIERAĆ ADRES DOCELOWEGO ODBIORCY
    n = len(trajectory)
    for i in range(n):
        lista = [trajectory[n-1-i], lista]
    return json.dumps(lista)

def send(ip, string_message):
    """TODO: socket"""
    pass
def receive():
    connection, address = s.accept()
    print("Accepted connection from {}".format(address))
    print(5*"=")
    while 1:
        data = connection.recv(1000)
        if not data: break
        print(str(data, 'utf-8'))
        connection.sendall(data)
    connection.close()
    print(5*"=")
    encoded_list = "ENCODED_LIST_GOES_HERE"
    origin_ip = address #from socket
    return encoded_list, origin_ip

def pass_along(encoded_list):
    """
        main node\endpoint behavior
        if length of list is 2, list contains
                * IP of next node
                * list of next steps (to be sent)
            encodes list with json and sends ahead
            then waits for reply and sends message back
        else if length of list is 1, list is message
            print message
            send "acknowledge" to last sender
            kill this process
    """
    #wait
    encoded_list, origin_ip = receive()
    received = json.loads(encoded_list)
    if len(received) == 2:
        udp_target, paczka = received
        paczka = json.dumps(paczka)
        send(nodes[udp_target], paczka)
        #wait #może wieloprocesowo
    elif len(received) == 1:
        wiadomosc = received
        print(wiadomosc)
        send(origin_ip, ACKNOWLEDGED)
        #commit seppuku
if __name__ == "__main__":
    s.listen(1)
    print(receive())
    s.close()
