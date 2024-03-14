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


import socket

# Configurações do servidor
HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 12347        # Porta do servidor
BUFFER_SIZE = 1024  # Tamanho do buffer
TIMEOUT = 2         # Tempo de timeout em segundos

# Criando os sockets UDP para enviar e receber mensagens / receber ACKs
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv_ACK_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Associando os sockets aos endereços e portas
udp_socket.bind((HOST, PORT))
recv_ACK_socket.bind((HOST, PORT+1))

# Declaraçao de funções utilizadas
def receber_ack(menssagem):
    for _ in range(100):  
        udp_socket.sendto(menssagem.encode(), addr)
        if esperando_timeout_ack(recv_ACK_socket):
            break

def esperando_timeout_ack(socket):
    while True:
        socket.settimeout(TIMEOUT)
        try: 
            ack, _ = socket.recvfrom(BUFFER_SIZE)
            if ack.decode() == "ACK":
                print('Recebi o ACK')
                return True
        except socket.timeout:
            return False
        
def visualizar_matriz(matriz):          # Função para visualizar a matriz de ocupação
    for dia in range(num_dias):
        print(f"Dia: {nome_dias[dia]}:")
        for sala in range(num_salas):
            for horario in range(num_horarios):
                ocupante = matriz[sala][dia][horario]
                print(f"Sala: {nome_salas[sala]}, Horário {nome_horarios[horario]}: {ocupante if ocupante else 'Vazia'}")
    print("\n")

# Definição da lista de Salas, Dias e Horarios possiveis 
num_salas = 5
nome_salas = ["E101", "E102","E103", "E104", "E105"]
num_dias = 5
nome_dias = ["seg", "ter", "qua", "qui", "sex"]
num_horarios = 9
nome_horarios = ["08h", "09h", "10h", "11h", "12h", "13h", "14h", "15h", "16h"]

# Inicializando a matriz com valores padrão (por exemplo, "vazia")
matriz_ocupacao = [[[None for _ in range(num_horarios)] for _ in range(num_dias)] for _ in range(num_salas)]

# Lista de usuários conectados
lista_usuarios = []

# Main
print('Servidor UDP pronto para receber arquivos...')
while True:
    data, addr = udp_socket.recvfrom(BUFFER_SIZE)    # Eecebendo o dado e endereço do cliente que enviou
    addrACK = (addr[0],(addr[1]+1))                  # Adicionando 1 para enviar ACK para a porta correta de recebimento
    udp_socket.sendto("ACK".encode(), addrACK)       # Enviar ACK para o cliente
    print(f'Enviando ACK para {addrACK}')
    
    frase = []                                      # Leitura do comando do cliente
    frase = data.decode()                           # Hora - 3 char, dia - 3 char, sala - 4char
    frase = frase.strip()
    frase = frase.split(' ')
    print(frase)
    
    match frase[0].lower():
        case 'connect':
            if frase[2] and frase[3]:

                nome_completo = f'{frase[2]} {frase[3]}'
                print(f'Chegou mais 1 usuário: {nome_completo} no IP: {addr}')
                menssagem = 'Você se conectou!'
                lista_usuarios.append((nome_completo, addr))
                receber_ack(menssagem)
                # Enviar menssagem para todos os outros clientes
                for tupla in lista_usuarios:
                    if tupla[1] != addr:
                        menssagem = f'{nome_completo} acabou de se conectar ao servidor'
                        receber_ack(menssagem)
            else:
                menssagem = 'O comando connect precisa ter um nome composto de 2 palavras. Ex: \'connect as Pedro Miguel\''
                receber_ack(menssagem)
        case 'bye':
            menssagem = 'Thau'
            for tupla in lista_usuarios[:]:  # Usando uma cópia da lista para evitar problemas de iteração
                if addr in tupla:
                    lista_usuarios.remove(tupla)
                    nome_completo = tupla[0]
                    print(f"Adeus Imundice {tupla[0]}")
            receber_ack(menssagem)
            # Enviar menssagem para todos os outros clientes
            for tupla in lista_usuarios:
                if tupla[1] != addr:
                    menssagem = f'{nome_completo} acabou de se desconectar do servidor'
                    receber_ack(menssagem)

        case 'list':
            print("Toma a lista")
            menssagem = f'A lista : {lista_usuarios}'
            receber_ack(menssagem)

        case 'reservar':
            flag = 0
            if (frase[1] != None and frase[2] != None and frase[3] != None and frase[1].upper() in nome_salas and frase[2].lower() in nome_dias and frase[3].lower() in nome_horarios):
                for tupla in lista_usuarios[:]:  # Usando uma cópia da lista para evitar problemas de iteração
                    if addr in tupla:
                        nome_completo = tupla[0]
                        flag = 1
                        salaDesejada = nome_salas.index(frase[1].upper())
                        diaDesejado = nome_dias.index(frase[2].lower())
                        horarioDesejado = nome_horarios.index(frase[3].lower())
                        if matriz_ocupacao[salaDesejada][diaDesejado][horarioDesejado] == None:
                            menssagem = 'Sala Reservada'
                            receber_ack(menssagem)
                            matriz_ocupacao[salaDesejada][diaDesejado][horarioDesejado] = tupla
                            # Enviar menssagem para todos os outros clientes
                            for tuplas in lista_usuarios:
                                if tuplas[1] != addr:
                                    menssagem = f'{nome_completo} acabou de reservar a sala: {frase[1]} no dia {frase[2]} as {frase[3]}'
                                    receber_ack(menssagem)
                        else:
                            menssagem = f'Essa sala já foi reservada por {(matriz_ocupacao[salaDesejada][diaDesejado][horarioDesejado])[0]}'
                            receber_ack(menssagem)
            
                            
                if flag == 0:   
                    menssagem = 'Você não está conectado'
                    receber_ack(menssagem)
            else:
                menssagem = 'Comando errado'
                receber_ack(menssagem)

        case 'cancelar':
            flag = 0
            if frase[1] != None and frase[2] != None and frase[3] != None  and frase[1].upper() in nome_salas and frase[2].lower() in nome_dias and frase[3].lower() in nome_horarios:
                for tupla in lista_usuarios[:]:  
                    if addr in tupla:
                        flag = 1
                        nome_completo = tupla[0]
                        salaDesejada = nome_salas.index(frase[1].upper())
                        diaDesejado = nome_dias.index(frase[2].lower())
                        horarioDesejado = nome_horarios.index(frase[3].lower())
                        if matriz_ocupacao[salaDesejada][diaDesejado][horarioDesejado] == tupla:
                            menssagem = 'Reserva cancelada'
                            receber_ack(menssagem)
                            matriz_ocupacao[salaDesejada][diaDesejado][horarioDesejado] = None
                            for tuplas in lista_usuarios:
                                if tuplas[1] != addr:
                                    menssagem = f'{nome_completo} acabou de cancelar a reserva da sala: {frase[1]} no dia {frase[2]} as {frase[3]}'
                                    receber_ack(menssagem)
                        else:
                            menssagem = f'Você não reservou essa sala!'
                            receber_ack(menssagem)
                            
                if flag == 0:   
                    menssagem = 'Você não está conectado'
                    receber_ack(menssagem)
                    udp_socket.sendto(menssagem.encode(), addr)
            else:
                menssagem = 'Comando errado'
                receber_ack(menssagem)
                    
        case 'check':
            lista_disponivel = []
            flag = 0
            if frase[1] != None and frase[2] != None and frase[1].upper() in nome_salas and frase[2].lower() in nome_dias:
                for tupla in lista_usuarios[:]:  
                    if addr in tupla:
                        flag = 1
                        salaDesejada = nome_salas.index(frase[1].upper())
                        diaDesejado = nome_dias.index(frase[2].lower())
                        for i in range(num_horarios):
                            if matriz_ocupacao[salaDesejada][diaDesejado][i] == None:
                                lista_disponivel.append(nome_horarios[i])
                 
                if flag == 0:   
                    menssagem = 'Você não está conectado'
                    receber_ack(menssagem)
                    
                if lista_disponivel == [] and flag == 1:
                    menssagem = 'Não há horários disponíveis'
                    receber_ack(menssagem)

                if lista_disponivel != []:
                    menssagem = f'{lista_disponivel}'
                    receber_ack(menssagem)
            else:
                menssagem = 'Comando errado'
                receber_ack(menssagem)
        case _ :
            print ("Comando errado")
            menssagem = 'Comando errado'
            receber_ack(menssagem)
            






