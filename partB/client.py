from socket import socket, AF_INET, SOCK_DGRAM
from sys import argv

PACKET_SIZE, CHUNK_SIZE, HEADER_SIZE = 100, 90, 10


def validate_port(port: int) -> None:
    """
    Validates that a given number is a port.
    :param port: the given number.
    :raise ValueError if the port is invalid.
    """
    if not 0 <= port < 2 ** 16:
        raise ValueError('Invalid port.')


def validate_ipv4(ip: str) -> None:
    """
    Validates that a given string is an ipv4 address.
    :param ip: the given string.
    :raise ValueError: if the ip is invalid.
    """
    if len(ip.split('.')) != 4 or not (number.isdigit() and 0 < int(number) < 255 for number in ip.split('.')):
        raise ValueError('Invalid IP.')


def validate_argv(params: int) -> None:
    """
    Validates that argv has a specified amount of parameters.
    :param params: the amount.
    :raise ValueError: if there aren't exactly params parameters in argv.
    """
    if len(argv) != params + 1:
        raise ValueError(f'Exactly {params} arguments are necessary, {len(argv) - 1} were inserted.')


def send_and_get_returned_file(addr: tuple[str, int], path: str) -> None:
    """
    Sends the file in the given path through UDP socket to the given address.
    :param addr: the given address.
    :param path: the given file path.
    :raise FileNotFoundError: if the given path isn't a file's path.
    """
    try:
        f = open(path)
        contents = f.read()
        f.close()
    except FileNotFoundError:
        raise FileNotFoundError("Couldn't find file.")
    s = socket(AF_INET, SOCK_DGRAM)
    s.settimeout(0.25)
    seen_package_nums = []
    for i in range(0, len(contents), CHUNK_SIZE):
        chunk, packet_number = contents[i:i + CHUNK_SIZE], i // CHUNK_SIZE
        while packet_number not in seen_package_nums:
            s.sendto(f'{packet_number:0{HEADER_SIZE}}{chunk}'.encode(), addr)
            try:
                data, source_addr = s.recvfrom(PACKET_SIZE)
                non_binary_data = data.decode('utf-8')
                place = int(non_binary_data[:HEADER_SIZE])
                seen_package_nums.append(place)
            except OSError:
                pass
    s.close()


def main():
    try:
        validate_argv(3)
        port, ip, file_path = int(argv[1]), argv[2], argv[3]
        validate_port(port)
        validate_ipv4(ip)
        dest_addr = (ip, port)
        send_and_get_returned_file(dest_addr, file_path)
    except Exception as e:
        print(e)


if '__main__' == __name__:
    main()
