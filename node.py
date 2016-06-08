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


def node_persistent_behavior(s):
    last_origin_ip = 0
    while True:
        try:
            received_string, origin_ip = skt.receive(s)
            print("String: {}".format(received_string))
        except:
            continue
        if "ADD_USER" in received_string:
            username = received_string[len("ADD_USER"):]
            if username not in users:
                print("Nowy użytkownik!", origin_ip, username)
            users[username] = origin_ip
        elif skt.ACKNOWLEDGED == received_string:
            print("Dostałem ACK od {}".format(origin_ip))
        else:
            received_list = json.loads(received_string)

            udp_target, paczka = received_list
            paczka = json.dumps(paczka)
            if udp_target not in skt.nodes:
                if udp_target in users:
                    target = users[udp_target]
            else:
                target = skt.nodes[udp_target]
                print("Wysyłam {} do {}: {}".format(paczka, udp_target, target))
                skt.send(s, paczka, target)



while(True):
    node_persistent_behavior(s)
    # p = multiprocessing.Process(target=node_persistent_behavior, args=(s,))
    # p.start()
s.close()
