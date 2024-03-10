import socket
import random
import threading

SERVER_HOST = '127.0.0.1'  # Endereço IP do servidor
SERVER_PORT = 12347         # Porta do servidor
CLIENT_PORT = random.randint(10000, 19999)  # Porta do cliente
BUFFER_SIZE = 1024          # Tamanho do buffer
TIMEOUT = 2                 # Tempo de timeout em segundos

#print(CLIENT_PORT)
#print((CLIENT_PORT+1))

# Criando o socket UDP para enviar mensagens
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.bind(('0.0.0.0', CLIENT_PORT))

# Criando o socket UDP para receber ACKs
recv_ACK_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv_ACK_socket.bind(('0.0.0.0', CLIENT_PORT + 1))

encerramento = threading.Event()  # Inicia o sistema de threads para receber e enviar mensagens

def receber_mensagens(socket):
    while not encerramento.is_set():
        file_data, origem = socket.recvfrom(BUFFER_SIZE)
        resposta = file_data.decode()
        print(resposta)
        addrACK = (origem[0],(origem[1]+1))
        client_socket.sendto("ACK".encode(), addrACK) 
        if resposta == "Thau":
            encerramento.set()
        print("Digite seu comando:")

thread_recebimento = threading.Thread(target=receber_mensagens, args=(client_socket,), daemon=True)
thread_recebimento.start()

def receber_ack():
    while not encerramento.is_set():
        recv_ACK_socket.settimeout(TIMEOUT)
        try: 
            ack, _ = recv_ACK_socket.recvfrom(BUFFER_SIZE)
            if ack.decode() == "ACK":
                print('Recebi o ACK')
                return True
        except socket.timeout:
            return False


print("Digite seu comando:\n")
while True:
    message = input()
    for _ in range(100):  # Número de tentativas
        client_socket.sendto(message.encode(), (SERVER_HOST, SERVER_PORT))
        if receber_ack():
            break

    if encerramento.is_set():  # Se a thread de recebimento terminou, saia do loop
        break

# Fechando os sockets                                                                             
client_socket.close()
recv_ACK_socket.close()
