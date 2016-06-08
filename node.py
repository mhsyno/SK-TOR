import json
import socket
import argparse
import sktor as skt
import multiprocessing
import time
import os

parser = argparse.ArgumentParser(description='Lorem ipsum!')
parser.add_argument('current_node_ID', type=int, nargs='+',
                    help="this node's ID")
args = parser.parse_args()
current_node_ID,  = args.current_node_ID

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(skt.nodes[current_node_ID])
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print("Listening on {}".format(skt.nodes[current_node_ID]))

users = {}

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
    encoded_list, origin_ip = skt.receive(s)
    received = json.loads(encoded_list)
    if len(received) == 2:
        udp_target, paczka = received
        paczka = json.dumps(paczka)
        skt.send(skt.nodes[udp_target], paczka)
        #wait #może wieloprocesowo
    elif len(received) == 1:
        wiadomosc = received
        print(wiadomosc)
        skt.send(origin_ip, skt.ACKNOWLEDGED)
        #commit seppuku


def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())


def receiver(connection, address, s):
    received_string, origin_ip = (skt.receive(connection, address))
    if "ADD_USER" in received_string:
        username = received_string[len("ADD_USER"):]
        print("Nowy użytkownik!", origin_ip, username)
    else:
        received_list = json.loads(received_string)
        if len(received_list) == 2:
            wiadomosc = received_list[0]
            print("Wiadomość z IP {}, oryginalnie od {}".format(origin_ip, "nie wiemy kto"))
            print(wiadomosc)
            skt.send(origin_ip, skt.ACKNOWLEDGED)
        elif len(received_list) == 2:
            udp_target, paczka = received_list
            paczka = json.dumps(paczka)
            print("Wysyłam {} do {}".format(paczka, skt.nodes[udp_target]))
            skt.send(skt.nodes[udp_target], paczka)
            print("Czekam")
            received_ack_message, ack_ip = skt.receive(*(skt.nodes[udp_target]))
            print("Dostałem {} do {}".format(received_ack_message, ack_ip))


s.listen(1)
while True:
    # pętla która przyjmuje połączenia i zaraz je przesyła do innego wątku
    connection, address = s.accept()
    p = multiprocessing.Process(target=receiver,
                                args=(connection, address, s))
    p.start()
    # p.join()
s.close()
