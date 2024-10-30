import socket

serverIP = '192.168.0.34'
serverPort = 2222
bufferSize = 1024
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    while True:
        message = input('Enter message to send to server (type "exit" to quit): ')
        if message.lower() == 'exit':
            break
            
        clientSocket.sendto(message.encode('utf-8'), (serverIP, serverPort))
        response, _ = clientSocket.recvfrom(bufferSize)
        print(f'Response from server: {response.decode("utf-8")}')
finally:
    clientSocket.close()
