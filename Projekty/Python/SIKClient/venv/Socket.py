import socket

s = socket.socket()  # Create a socket object
#host = input("Podaj adres ip: ")  # Get local machine name
host = '127.0.0.1'
port = 2137 # Reserve a port for your service.
response = 'st'
if (s.connect_ex((host, port)) == 0):
    response = s.recv(2)
    f = open('Winner.pdf', 'wb')
    size = int.from_bytes(s.recv(4), byteorder="big")
    remaining_bytes = socket.ntohl(size)
    print("Wielkość pliku =", remaining_bytes)

    toSent = 512
    while (remaining_bytes>0):
        if (remaining_bytes < toSent):
            toSent = remaining_bytes
        l = s.recv(toSent)
        f.write(l)
        remaining_bytes = remaining_bytes - toSent
        print("Receiving...")




    f.close()
    # if (response.decode() == "p1"):
    #     answer = input()
    #     answer = answer.encode()
    #     s.sendall(answer)


        # receive info on answer success

    #     response = s.recv(2)
    #     response = response.decode()
    #     if (response == 'ok'):
    #         print('Hit')
    #     elif (response == 'no'):
    #         print('Miss')
    #     response = ''
    # else:
    #     response = s.recv(2)
    #     response = response.decode()
    #     if (response == 'ok'):
    #         print('Opponent has hit one of your units')
    #     elif (response == 'no'):
    #         print('Opponent has missed')
    #     # input answer
    #
    #     answer = input()
    #     answer = answer.encode()
    #     s.sendall(answer)
    #
    #     # receive info on answer success
    #
    #     response = s.recv(2)
    #     response = response.decode()
    #     if (response == 'ok'):
    #         print('Hit')
    #     elif (response == 'no'):
    #         print('Miss')
    #     response = ''
    #


    # while (response != 'dn'):
    #     ## receive info on enemy move status
    #
    #     response = s.recv(2)
    #     response = response.decode()
    #     if (response == 'ok'):
    #         print('Opponent has hit one of your units')
    #     elif (response == 'no'):
    #         print('Opponent has missed')
    #     # input answer
    #
    #     answer = input()
    #     answer = answer.encode()
    #     s.sendall(answer)
    #
    #     # receive info on answer success
    #
    #     response = s.recv(2)
    #     response = response.decode()
    #     if (response == 'ok'):
    #         print('Hit')
    #     elif (response == 'no'):
    #         print('Miss')
    #     response = ''
else:
    print("kek")
s.close