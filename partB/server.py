from socket import socket, AF_INET, SOCK_DGRAM, error
from sys import argv
from client import HEADER_SIZE, PACKET_SIZE


def infinitely_receive_and_print(s):
    printed = []
    while True:
        data, source_addr = s.recvfrom(PACKET_SIZE)
        non_binary_data = data.decode('utf-8')
        place = int(non_binary_data[:HEADER_SIZE])
        while place not in printed:
            print(non_binary_data[HEADER_SIZE:], end="", flush=True)
            printed.append(place)
        s.sendto(data, source_addr)


def main():
    try:
        if len(argv) != 2:
            raise ValueError(f'Exactly 1 arguments are necessary, {len(argv) - 1} were inserted.')
        my_port = int(argv[1])
        s = socket(AF_INET, SOCK_DGRAM)
        s.bind(('', my_port))
        infinitely_receive_and_print(s)
        s.close()
    except (ValueError, error) as e:
        print(e)


if "__main__" == __name__:
    main()
