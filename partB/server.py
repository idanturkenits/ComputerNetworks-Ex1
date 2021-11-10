from socket import socket, AF_INET, SOCK_DGRAM
from sys import argv
from client import HEADER_SIZE, PACKET_SIZE, validate_port, validate_argv


def infinitely_receive_and_print(s: socket) -> None:
    """
    Infinitely receives, prints and resends packets.
    :param s: the UDP socket that the packets go through.
    """
    printed = []
    while True:
        data, source_addr = s.recvfrom(PACKET_SIZE)
        non_binary_data = data.decode('utf-8')
        place = int(non_binary_data[:HEADER_SIZE])
        while place not in printed:
            print(non_binary_data[HEADER_SIZE:], end='', flush=True)
            printed.append(place)
        s.sendto(data, source_addr)


def main():
    try:
        validate_argv(1)
        my_port = int(argv[1])
        validate_port(my_port)
        s = socket(AF_INET, SOCK_DGRAM)
        s.bind(('', my_port))
        infinitely_receive_and_print(s)
        s.close()
    except Exception as e:
        print(e)


if '__main__' == __name__:
    main()
