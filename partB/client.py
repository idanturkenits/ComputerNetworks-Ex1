from socket import socket,AF_INET,SOCK_DGRAM
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
    i = 1
    for chunk in [contents[i:i+chunk_size] for i in range(0, len(contents), chunk_size)]:
        received = False
        while(received == False):
            s.sendto((((10 - len(str(i))) * '0') + str(i) + str(chunk)).encode(), addr)
            try:
                data, source_addr = s.recvfrom(100)
                final = final + str(data.decode("utf-8"))[10:]
                received = True
                i = i + 1
            except:
                pass

    return final

def check_return(returned_string, file_path):   
    with open(file_path) as f:
        if(f.read() == returned_string):
            print("return is good")
            exit()
       

s = socket(AF_INET,SOCK_DGRAM)
s.settimeout(0.01)
returned = send_and_get_returned_file(DEST_ADDR, FILE_PATH)
check_return(returned, FILE_PATH)
