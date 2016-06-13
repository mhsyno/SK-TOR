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

WAITING_FOR_ACK = False
WAITING_FOR_ACK_MESSAGE = ""
def listen(s):
    global WAITING_FOR_ACK, WAITING_FOR_ACK_MESSAGE
    while True:
        data, origin_ip = skt.receive(s)
        if data.startswith(skt.LIST_USERS):
            print("CURRENT USERS:\n" + data[len(skt.LIST_USERS):])
        elif WAITING_FOR_ACK and data.startswith(skt.ACKNOWLEDGED):
            print("Received acknowledgment for message: {}".format(WAITING_FOR_ACK_MESSAGE))
            WAITING_FOR_ACK = False
            WAITING_FOR_ACK_MESSAGE = False
        else:
            print("\nCLIENT: Recieved {} bytes:\n=====\n{}\n=====".format(len(data), data))
            skt.send(s, skt.ACKNOWLEDGED, origin_ip)


def send(s):
    global WAITING_FOR_ACK, WAITING_FOR_ACK_MESSAGE
    while True:
        target = input("Message recipient: ")
        message = input("Your message: ") #python3 has a new "bytes" data type
        if message is "END":
            break
        target, trajectory = skt.prep_trajectory(message, target, users_name)
        # print(target, skt.nodes[target], trajectory)
        skt.send(s, trajectory, skt.nodes[target])
        WAITING_FOR_ACK = True
        WAITING_FOR_ACK_MESSAGE = message

        # musi czekać na


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.settimeout(9999999)
    for key in skt.nodes:
        users_name_as_bytes = bytes("ADD_USER" + users_name, encoding='utf-8')
        s.sendto(users_name_as_bytes, skt.nodes[key])



    listener = multiprocessing.Process(target=listen,
                                args=(s,))
    listener.start()

    send(s)
