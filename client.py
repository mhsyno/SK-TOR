# -*- coding: utf-8 -*-

import socket
import argparse
import sktor as skt

parser = argparse.ArgumentParser(description='Lorem ipsum!')
parser.add_argument('current_node_ID', type=int, nargs='+',
                    help="this node's ID")
parser.add_argument('target_ID', type=int, nargs='+',
                    help="recipient_ID")
args = parser.parse_args()
current_node_ID, target_ID = args.current_node_ID[0], args.target_ID[0]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(skt.nodes[current_node_ID])
    s.connect(skt.nodes[target_ID])
    data = bytes(input("Your message: "), encoding='utf-8') #python3 has a new "bytes" data type
    s.send(data)
    data = str(s.recv(1000), 'utf-8')
    print("CLIENT: Recieved {} bytes:\n=====\n{}\n=====".format(len(data), data))
