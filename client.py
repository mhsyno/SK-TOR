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

users_name = "ADD_USER" + input("Type in your name: ")

for key in skt.nodes:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect(skt.nodes[key])
        users_name_as_bytes = bytes(users_name, encoding='utf-8')
        s.send(users_name_as_bytes)


message = input("Your message: ") #python3 has a new "bytes" data type
prepared_trajectory = skt.prep_trajectory(skt.n)
encoded_trajectory = skt.encode_trajectory(prepared_trajectory, message,
    target_ID, current_node_ID)
print(encoded_trajectory)
udp_target, encoded_trajectory = encoded_trajectory
trajectory_as_bytes = bytes(encoded_trajectory, encoding='utf-8')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # s.bind(skt.nodes[current_node_ID])
    s.connect(skt.nodes[udp_target])
    s.send(trajectory_as_bytes)
    data = str(s.recv(1000), 'utf-8')
    print("CLIENT: Recieved {} bytes:\n=====\n{}\n=====".format(len(data), data))
