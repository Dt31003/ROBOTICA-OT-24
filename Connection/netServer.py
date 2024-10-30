import socket
import subprocess

bufferSize = 1024
serverPort = 2222
serverIP = '192.168.0.34'

RPIsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
RPIsocket.bind((serverIP, serverPort))

print('Server is UP and Listening...')

while True:
    message, address = RPIsocket.recvfrom(bufferSize)
    command = message.decode('utf-8')

    print('Received command:', command)
    print('Client Address:', address[0])

    if command.lower() == 'exit':
        print('Closing server...')
        break

    try:
        # Ejecutar el comando en la terminal
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        response = result.stdout if result.returncode == 0 else result.stderr  # Capturar solo stdout o stderr según el resultado
    except Exception as e:
        response = str(e)

    # Enviar respuesta al cliente
    RPIsocket.sendto(response.encode('utf-8'), address)

RPIsocket.close()
