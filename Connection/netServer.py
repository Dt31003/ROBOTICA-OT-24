import socket

bufferSize = 1024
serverPort = 2222
serverIP = '192.168.0.34'
RPIsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
RPIsocket.bind((serverIP, serverPort))

print('Server is UP and Listening...')

while True:
    message, address = RPIsocket.recvfrom(bufferSize)
    message = message.decode('utf-8')
    
    print(f'Message from client: {message}')
    print('Client Address:', address[0])
    
    # Aquí puedes procesar el mensaje y decidir qué comando enviar
    response = f'Server received: {message}'
    RPIsocket.sendto(response.encode('utf-8'), address)
