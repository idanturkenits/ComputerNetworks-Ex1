from socket import socket, AF_INET, SOCK_DGRAM
from sys import argv
from client import HEADER_SIZE, PACKET_SIZE


def main():
    my_port = int(argv[1])
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(('', my_port))
    printed = []
    seen = dict()
    i = 1
    while True:
        data, source_addr = s.recvfrom(PACKET_SIZE)
        non_binary_data = data.decode('utf-8')
        place = int(non_binary_data[:HEADER_SIZE])
        seen[place] = non_binary_data[HEADER_SIZE:]
        while i in seen and i not in printed:
            print(seen[i], end="", flush=True)
            printed.append(i)
            i = i + 1
        s.sendto(data, source_addr)


if "__main__" == __name__:
    main()
