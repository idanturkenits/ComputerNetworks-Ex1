from socket import socket, AF_INET, SOCK_DGRAM, error
from sys import argv

PACKET_SIZE, CHUNK_SIZE, HEADER_SIZE = 100, 90, 10


def send_and_get_returned_file(addr, file):
    try:
        f = open(file)
        contents = f.read()
        f.close()
    except FileNotFoundError:
        raise FileNotFoundError("Couldn't find file.")
    s = socket(AF_INET, SOCK_DGRAM)
    s.settimeout(1)
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
        if len(argv) != 4:
            raise ValueError(f'Exactly 3 arguments are necessary, {len(argv) - 1} were inserted.')
        dest_addr = (argv[2], int(argv[1]))
        file_path = argv[3]
        send_and_get_returned_file(dest_addr, file_path)
    except (FileNotFoundError, ValueError, error) as e:
        print(e)


if "__main__" == __name__:
    main()
