import socket
import random
import threading
from rdt import *


SERVER_HOST = '127.0.0.1'  # Endereço IP do servidor
SERVER_PORT = 12347        # Porta do servidor
CLIENT_PORT = random.randint(10000, 19999)       # Porta do cliente
BUFFER_SIZE = 1024         # Tamanho do buffer
TIMEOUT = 2                # Tempo de timeout em segundos
# Criando o socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Associa o socket do cliente a uma porta específica
client_socket.bind(('0.0.0.0', CLIENT_PORT))

encerramento = threading.Event()      # iniciando o sistemas de threads para receber e enviar msgs

def receber_mensagens(socket):
    while True:
        file_data, origem = socket.recvfrom(BUFFER_SIZE)
        resposta = file_data.decode()
        print(resposta)
        print("Digite seu comando:")
        if resposta == "Thau":
            encerramento.set()        # sinaliza que esta thread de recebimento terminou sua execuçao
            break                     

thread_recebimento = threading.Thread(target=receber_mensagens, args=(client_socket,), daemon=True)
thread_recebimento.start()

print("Digite seu comando:\n")
while True:
    message = str(input())
     # Enviar mensagem com timeout e retry
    for _ in range(3):  # Número de tentativas
        client_socket.sendto(message.encode(), (SERVER_HOST, SERVER_PORT))
        client_socket.settimeout(TIMEOUT)
        try:
            ack, _ = client_socket.recvfrom(BUFFER_SIZE)
            if ack.decode() == "ACK":
                break  # Sai do loop se receber um ACK bem-sucedido
        except socket.timeout:
            print("Timeout! Tentando novamente...")

    if encerramento.is_set():                #se esta thread de recebimento acabou sua execuçao, nossa thread main também vai                                                                               
        break

# Fechando o socket
                                                                                               
client_socket.close()

""" def send_with_retransmission(socket, message, server_address, timeout=2):
    try:
        # Envia a mensagem
        socket.sendto(message.encode(), server_address)
        print("Mensagem enviada, esperando ACK...")

        # Define o timeout para esperar pela resposta (ACK)
        socket.settimeout(timeout)

        # Tenta receber o ACK
        while True:
            try:
                data, server = socket.recvfrom(1024)
                ack = data.decode()
                print("ACK recebido:", ack)
                break  # Sai do loop após receber ACK
            except socket.timeout:
                print("Timeout, retransmitindo...")
                socket.sendto(message.encode(), server_address)
    except KeyboardInterrupt:
        pass """
