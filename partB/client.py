from socket import socket, AF_INET, SOCK_DGRAM
import sys

DEST_PORT = int(sys.argv[1])
DEST_IP = sys.argv[2]
FILE_PATH = sys.argv[3]
DEST_ADDR = (DEST_IP, DEST_PORT)


def send_and_get_returned_file(addr, file):
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
                place = non_binary_data[0:10]
                if int(place) not in seen:
                    seen[int(place)] = non_binary_data[10:]
                    amount_chunks_got = amount_chunks_got + 1
                if(number_of_packet == int(place)):
                    number_of_packet = number_of_packet + 1
                    received = True
            except:
                pass
    
    for x in sorted(seen.keys()):
        final = final + seen[x]
    return final


def check_return(returned_string, file_path):
    with open(file_path) as f:
        if f.read() == returned_string:
            print("return is good")
            exit()
            

s = socket(AF_INET, SOCK_DGRAM)
s.settimeout(0.005)
returned = send_and_get_returned_file(DEST_ADDR, FILE_PATH)
check_return(returned, FILE_PATH)
