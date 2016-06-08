import json
import socket
import argparse
import sktor as skt

parser = argparse.ArgumentParser(description='Lorem ipsum!')
parser.add_argument('current_node_ID', type=int, nargs='+',
                    help="this node's ID")
args = parser.parse_args()
current_node_ID,  = args.current_node_ID

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(skt.nodes[current_node_ID])
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print("Listening on {}".format(skt.nodes[current_node_ID]))

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

s.listen(1)
while True:
    # pętla która przyjmuje połączenia
    # zaraz je przesyła
    connection, address = s.accept()
    print(skt.receive(connection, address))
s.close()
