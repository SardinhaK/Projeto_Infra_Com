import socket
import os

SERVER_HOST = '127.0.0.1'  # Endereço IP do servidor
SERVER_PORT = 12347        # Porta do servidor
CLIENT_PORT = 12348        # Porta do cliente
BUFFER_SIZE = 1024         # Tamanho do buffer
TIMEOUT = 2                # Tempo de timeout em segundos

# Mudando o diretório de trabalho para onde os arquivos estão
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Lista de nomes de arquivos a serem enviados
filenames = ['mensagem.txt', 'imagem.jpeg']

# Criando o socket UDP
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Associa o socket do cliente a uma porta específica
udp_socket.bind(('0.0.0.0', CLIENT_PORT))

# Enviando solicitações para cada arquivo
for filename in filenames:
    # Lendo o conteúdo do arquivo
    with open(filename, 'rb') as file:
        file_data = file.read()

    # Enviando o nome do arquivo para o servidor
    udp_socket.sendto(filename.encode(), (SERVER_HOST, SERVER_PORT))

    # Enviando o conteúdo do arquivo para o servidor
    udp_socket.sendto(file_data, (SERVER_HOST, SERVER_PORT))

    # Configurando o timeout
    udp_socket.settimeout(TIMEOUT)

    while True:
        try:
            # Recebendo o arquivo de volta do servidor com o nome modificado
            file_data, server_address = udp_socket.recvfrom(BUFFER_SIZE)
            break  # Se recebido com sucesso, sai do loop
        
        except socket.timeout:
            print(f"Timeout! Retransmitindo arquivo {filename}...")
            
            # Reenvia o nome do arquivo
            udp_socket.sendto(filename.encode(), (SERVER_HOST, SERVER_PORT))
            
            # Reenvia o conteúdo do arquivo
            udp_socket.sendto(file_data, (SERVER_HOST, SERVER_PORT))

    # Desativa o timeout após a transmissão bem-sucedida
    udp_socket.settimeout(None)

    # Salvando o arquivo recebido com o nome modificado
    filename_modified = f"{filename.split('.')[0]}_modificado.{filename.split('.')[1]}"
    with open(filename_modified, 'wb') as file:
        file.write(file_data)
        print(f"Arquivo {filename} recebido como {filename_modified}.")

# Fechando o socket
udp_socket.close()
