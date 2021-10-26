from socket import socket, AF_INET, SOCK_DGRAM
import sys


def send_and_get_returned_file(addr, file):
    s = socket(AF_INET, SOCK_DGRAM)
    s.settimeout(0.005)
    with open(file) as f:
        contents = f.read()
    
    final = ''
    chunk_size = 90
    amount_chunks_got = 0
    number_of_packet = 1
    seen = dict()
    for chunk in [contents[i:i + chunk_size] for i in range(0, len(contents), chunk_size)]:
        received = False
        if number_of_packet in seen:
            received = True
            amount_chunks_got = amount_chunks_got + 1
            number_of_packet = number_of_packet + 1
        while not received:
            s.sendto((((10 - len(str(number_of_packet))) * '0') + str(number_of_packet) + str(chunk)).encode(), addr)
            try:
                data, source_addr = s.recvfrom(100)
                non_binary_data = data.decode('utf-8')
                place = int(non_binary_data[0:10])
                if place not in seen:
                    seen[place] = non_binary_data[10:]
                    amount_chunks_got = amount_chunks_got + 1
                if number_of_packet == place:
                    number_of_packet = number_of_packet + 1
                    received = True
            except:
                pass
    s.close()
    for x in sorted(seen.keys()):
        final = final + seen[x]
    return final


def main():
    dest_port = int(sys.argv[1])
    dest_ip = sys.argv[2]
    file_path = sys.argv[3]
    dest_addr = (dest_ip, dest_port)
    send_and_get_returned_file(dest_addr, file_path)


if __name__ == "__main__":
    main()
