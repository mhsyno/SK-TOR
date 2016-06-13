# -*- coding: utf-8 -*-

import socket
import argparse
import sktor as skt
import multiprocessing
import json

# parser = argparse.ArgumentParser(description='Lorem ipsum!')
# parser.add_argument('this_ID', type=str, nargs='+',
#                     help="user's ID")
# parser.add_argument('target_ID', type=int, nargs='+',
#                     help="recipient's ID")
# parser.add_argument('message', type=str, nargs='+',
#                     help="message to be sent")
# args = parser.parse_args()
# users_name, target, message = args.this_ID[0], args.target_ID[0], args.message[0]

users_name = input("Type in your name: ")

def listen(s):
    while True:
        data, origin_ip = skt.receive(s)
        if data.startswith(skt.LIST_USERS):
            print("======\nCURRENT USERS:\n" + data[len(skt.LIST_USERS):] + "======\n")
        elif data.startswith(skt.ACKNOWLEDGED):
            print("\nReceived acknowledgment for message")
        elif data.startswith(skt.SEND_FAIL):
            print("\nSending message failed")
        else:
            print("\nCLIENT: Recieved {} bytes:\n=====\n{}\n=====".format(len(data), data))
            skt.send(s, skt.ACKNOWLEDGED, origin_ip)
def send(s):
    while True:
        target = input("Message recipient: ")
        message = input("Your message: ") #python3 has a new "bytes" data type
        if message is "END":
            break
        target, trajectory = skt.prep_trajectory(message, target, users_name)
        # print(target, skt.nodes[target], trajectory)
        skt.send(s, trajectory, skt.nodes[target])

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.settimeout(9999999)
    for key in skt.nodes:
        users_name_as_bytes = bytes("ADD_USER" + users_name, encoding='utf-8')
        s.sendto(users_name_as_bytes, skt.nodes[key])



    listener = multiprocessing.Process(target=listen,
                                args=(s,))
    listener.start()

    send(s)
