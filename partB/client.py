from socket import socket, AF_INET, SOCK_DGRAM
from sys import argv

PACKET_SIZE, CHUNK_SIZE, HEADER_SIZE = 100, 90, 10


def send_and_get_returned_file(addr, file):
    # setting up the client socket
    s = socket(AF_INET, SOCK_DGRAM)
    s.settimeout(0.005)
    
    # reading the contants from the file in order to send the client
    with open(file) as f:
        contents = f.read()
    
    # a variable to store the text that the server returned
    final = ''
    # keeping track of how many packets weve got
    amount_chunks_got = 0
    # keeping track of the number of packet we send
    number_of_packet = 1
    # keeping track of which packets weve got
    seen = dict()
    for i in range(0, len(contents), CHUNK_SIZE):
        # deviding the content of the file into 100 bytes chunks 
        chunk = contents[i:i + CHUNK_SIZE]
        received = False
        """ 
        if we already saw out packet, we dont need to send and receive it from server
        """
        if number_of_packet in seen:
            received = True
            amount_chunks_got = amount_chunks_got + 1
            number_of_packet = number_of_packet + 1
        while not received:
            # sending the packet to the server
            s.sendto(f'{number_of_packet:0{HEADER_SIZE}}{chunk}'.encode(), addr)
            try:
                # reaciving answer from server
                data, source_addr = s.recvfrom(PACKET_SIZE)
                non_binary_data = data.decode('utf-8')
                place = int(non_binary_data[:HEADER_SIZE])

                
                # we can get any packet from the server(becuase of the delay),so we store the
                # packets we are getting in the seen dictonary
                if place not in seen:
                    seen[place] = non_binary_data[HEADER_SIZE:]
                    amount_chunks_got = amount_chunks_got + 1
                
                # if we got the packet that we send, we can move on sending the next packet
                if number_of_packet == place:
                    number_of_packet = number_of_packet + 1
                    received = True
            
            # if the time for the reacive function ran out, 
            # we are sending the packet again to the server
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
