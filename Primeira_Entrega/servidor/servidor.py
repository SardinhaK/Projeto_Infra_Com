import socket

# Configurações do servidor
HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 12345        # Porta do servidor
BUFFER_SIZE = 1024  # Tamanho do buffer

# Diretório onde os arquivos serão armazenados


# Criando o socket UDP
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Associando o socket ao endereço e porta
udp_socket.bind((HOST, PORT))

print('Servidor UDP pronto para receber arquivos...')

while True:
    # Recebendo dados e endereço do cliente
    data, addr = udp_socket.recvfrom(BUFFER_SIZE)
    filename = data.decode()  # Convertendo os dados recebidos para o nome do arquivo

    # Recebendo o conteúdo do arquivo
    file_data, addr = udp_socket.recvfrom(BUFFER_SIZE)

    # Salvando o arquivo recebido
    with open(f'{filename}', 'wb') as file:
        file.write(file_data)
        print(f"Arquivo {filename} recebido e salvo com sucesso.")

    # Modificando o nome do arquivo para devolução
    filename_modified = f"{filename.split('.')[0]}_modificado.{filename.split('.')[1]}"

    # Lendo o arquivo salvo
    with open(f'{filename}', 'rb') as file:
        file_data = file.read()

    # Enviando o conteúdo do arquivo de volta para o cliente com o nome modificado
    udp_socket.sendto(file_data, addr)
    print(f"Arquivo {filename} enviado como {filename_modified} para {addr}")

# Fechando o socket
udp_socket.close()
