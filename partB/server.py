from socket import socket, AF_INET, SOCK_DGRAM, error
from sys import argv
from client import HEADER_SIZE, PACKET_SIZE


def infinitely_receive_and_print(s):
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
