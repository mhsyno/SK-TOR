import json
import socket
import argparse
import sktor as skt
import multiprocessing
import os
import time

parser = argparse.ArgumentParser(description='Lorem ipsum!')
parser.add_argument('current_node_ID', type=int, nargs='+',
                    help="this node's ID")
args = parser.parse_args()
current_node_ID,  = args.current_node_ID

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(skt.nodes[current_node_ID])
s.settimeout(99999)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print("Listening on {}".format(skt.nodes[current_node_ID]))

users = {}

def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

WAITING_FOR_ACK_IP = None
def node_persistent_behavior(s):
    global WAITING_FOR_ACK_IP
    while True:
        received_string, origin_ip = skt.receive(s)
        print("String: {}".format(received_string))
        if "ADD_USER" in received_string:
            username = received_string[len("ADD_USER"):]
            if username not in users:
                print("Nowy użytkownik!", origin_ip, username)
            users[username] = origin_ip

            if current_node_ID == 0:
                duzy_string = skt.LIST_USERS + "\n"
                for username in users:
                    duzy_string = duzy_string + username + "\n"

                for username in users:
                    skt.send(s, duzy_string, users[username])

        elif skt.ACKNOWLEDGED == received_string:
            print("Dostałem ACK od {}".format(origin_ip))
            # import ipdb; ipdb.set_trace()
            skt.send(s, skt.ACKNOWLEDGED, WAITING_FOR_ACK_IP)
        elif skt.SEND_FAIL == received_string:
            print("Dostałem SEND_FAIL od {}".format(origin_ip))
            skt.send(s, skt.SEND_FAIL, WAITING_FOR_ACK_IP)
        else:
            received_list = json.loads(received_string)

            target_username, paczka = received_list
            paczka = json.dumps(paczka)
            if target_username not in skt.nodes and target_username in users:
                target = users[target_username]
            else:
                try:
                    target = skt.nodes[target_username]
                except KeyError:
                    target = origin_ip
                    paczka = skt.SEND_FAIL
                    target_username = "poprzedni uzytkownik"
            print("Wysyłam {} do {}: {}".format(paczka, target_username, target))
            skt.send(s, paczka, target)
            WAITING_FOR_ACK_IP = origin_ip



while(True):
    node_persistent_behavior(s)
    # p = multiprocessing.Process(target=node_persistent_behavior, args=(s,))
    # p.start()
s.close()
