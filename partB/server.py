from socket import socket, AF_INET, SOCK_DGRAM
from sys import argv
from client import HEADER_SIZE, PACKET_SIZE


def main():
    # setting up port and socket
    my_port = int(argv[1])
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(('', my_port))
    # list to keep track of the packets we printed
    printed = []
    # list to  keep track of the packets we got
    seen = dict()
    i = 1
    while True:
        # getting a packet from the client
        data, source_addr = s.recvfrom(PACKET_SIZE)
        non_binary_data = data.decode('utf-8')
        place = int(non_binary_data[:HEADER_SIZE])
        # adding the data to the seen dictunary
        seen[place] = non_binary_data[HEADER_SIZE:]

        # if we have a packet with the packet
        # number that matches the order, and we didnt print it,
        # we print it and add it to the printed list
        while i in seen and i not in printed:
            print(seen[i], end="", flush=True)
            printed.append(i)
            i = i + 1

        # send the data back to the client
        s.sendto(data, source_addr)


if "__main__" == __name__:
    main()
