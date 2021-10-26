from socket import socket, AF_INET, SOCK_DGRAM
from sys import argv

PACKET_SIZE, CHUNK_SIZE, HEADER_SIZE = 100, 90, 10


def send_and_get_returned_file(addr, file):
    s = socket(AF_INET, SOCK_DGRAM)
    s.settimeout(0.005)
    with open(file) as f:
        contents = f.read()
    final = ''
    amount_chunks_got = 0
    number_of_packet = 1
    seen = dict()
    for i in range(0, len(contents), CHUNK_SIZE):
        chunk = contents[i:i + CHUNK_SIZE]
        received = False
        if number_of_packet in seen:
            received = True
            amount_chunks_got = amount_chunks_got + 1
            number_of_packet = number_of_packet + 1
        while not received:
            s.sendto(f'{number_of_packet:0{HEADER_SIZE}}{chunk}'.encode(), addr)
            try:
                data, source_addr = s.recvfrom(PACKET_SIZE)
                non_binary_data = data.decode('utf-8')
                place = int(non_binary_data[:HEADER_SIZE])
                if place not in seen:
                    seen[place] = non_binary_data[HEADER_SIZE:]
                    amount_chunks_got = amount_chunks_got + 1
                if number_of_packet == place:
                    number_of_packet = number_of_packet + 1
                    received = True
            except OSError:
                pass
    s.close()
    for x in sorted(seen.keys()):
        final = final + seen[x]
    return final


def main():
    dest_addr = (argv[2], int(argv[1]))
    file_path = argv[3]
    send_and_get_returned_file(dest_addr, file_path)


if "__main__" == __name__:
    main()
