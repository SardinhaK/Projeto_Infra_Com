import socket
import random


SERVER_HOST = '127.0.0.1'  # Endereço IP do servidor
SERVER_PORT = 12347        # Porta do servidor
CLIENT_PORT = random.randint(10000, 19999)       # Porta do cliente
BUFFER_SIZE = 1024         # Tamanho do buffer
TIMEOUT = 2                # Tempo de timeout em segundos
# Criando o socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Associa o socket do cliente a uma porta específica
client_socket.bind(('0.0.0.0', CLIENT_PORT))

while True:
    message  = str(input("Digite seu comando:\n"))                      
    client_socket.sendto(message.encode(), (SERVER_HOST, SERVER_PORT))
    file_data, server_address = client_socket.recvfrom(BUFFER_SIZE)
    resposta = file_data.decode()
    print(resposta)
    if resposta == 'Thau':
        break


# Fechando o socket

client_socket.close()
