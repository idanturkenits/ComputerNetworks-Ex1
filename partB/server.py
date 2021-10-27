from socket import socket, AF_INET, SOCK_DGRAM
from sys import argv
from client import HEADER_SIZE, PACKET_SIZE


def main():
    my_port = int(argv[1])
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(('', my_port))
    seen, printed, package_number = dict(), [], 0
    while True:
        data, source_addr = s.recvfrom(PACKET_SIZE)
        non_binary_data = data.decode('utf-8')
        place = int(non_binary_data[:HEADER_SIZE])
        seen[place] = non_binary_data[HEADER_SIZE:]
        while package_number in seen.keys() and package_number not in printed:
            print(seen[package_number], end="", flush=True)
            printed.append(package_number)
            package_number = package_number + 1
        s.sendto(data, source_addr)


if "__main__" == __name__:
    main()
