import json
from random import randint
import socket

nodes = {0: ["192.168.1.12", 5005], 1: ["192.168.1.17", 5005]} #adresy go here
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

def encode_trajectory(trajectory, message):
    """ takes trajectory list (use prep_trajectory) and string message

    returns trajectory and message as nested list in JSON string form
    """
    lista = message # string, ale ok
    n = len(trajectory)
    for i in range(n):
        lista = [trajectory[n-1-i], lista]
    return json.dumps(lista)

def send(ip, string_message):
    """TODO: socket"""
    pass
def receive():
    """TODO: socket"""
    encoded_list = ""
    origin_ip = ["192.168.1.12", 5005] #from socket
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
    # for i in range(20):
    #     print(encode_trajectory(prep_trajectory(n), "koczkodan"))
    pass
