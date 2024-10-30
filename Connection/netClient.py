import socket

serverIP = '192.168.0.34'
serverPort = 2222
bufferSize = 1024

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    command = input("Enter command to run on server (or 'exit' to quit): ")
    clientSocket.sendto(command.encode('utf-8'), (serverIP, serverPort))
    
    if command.lower() == 'exit':
        print('Exiting client...')
        break

    response, _ = clientSocket.recvfrom(bufferSize)
    print('Server response:', response.decode('utf-8'))

clientSocket.close()
