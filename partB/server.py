from socket import socket,AF_INET,SOCK_DGRAM
import sys

MY_PORT = int(sys.argv[1])

s = socket(AF_INET,SOCK_DGRAM)
s.bind(('',MY_PORT))

printed = []
while True:
    data, source_addr = s.recvfrom(100)
    non_binary_data = data.decode('utf-8')
    place = non_binary_data[0:10]
    text = non_binary_data[10:]
    if(not place in printed):
        print(text, end="", flush=True)
        printed.append(place)
    s.sendto(data, source_addr)