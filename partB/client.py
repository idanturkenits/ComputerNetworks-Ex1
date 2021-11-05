from socket import socket, AF_INET, SOCK_DGRAM
from sys import argv
PACKET_SIZE, CHUNK_SIZE, HEADER_SIZE = 100, 90, 10


def validate_port(port):
    if not 0 <= port < 2 ** 16:
        raise ValueError('Invalid port.')


def validate_ipv4(ip):
    if len(ip.split('.')) != 4 or not (number.isdigit() and 0 < int(number) < 255 for number in ip.split('.')):
        raise ValueError('Invalid IP.')
    

def validate_argv(params):
    if len(argv) != params + 1:
        raise ValueError(f'Exactly {params} arguments are necessary, {len(argv) - 1} were inserted.')


def send_and_get_returned_file(addr, file):
    try:
        f = open(file)
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
