from socket import socket, AF_INET, SOCK_DGRAM
import sys

MY_PORT = int(sys.argv[1])

s = socket(AF_INET, SOCK_DGRAM)
s.bind(('', MY_PORT))

printed = []
seen = dict()
i = 1
while True:
    data, source_addr = s.recvfrom(100)
    non_binary_data = data.decode('utf-8')
    place = non_binary_data[0:10]
    seen[int(place)] = non_binary_data
    while i in seen and i not in printed:
        print(seen[i][10:], end="", flush=True)
        printed.append(i)
        i = i + 1
    s.sendto(data, source_addr)
