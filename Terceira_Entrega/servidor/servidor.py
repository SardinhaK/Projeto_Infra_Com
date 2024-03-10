import socket

# Configurações do servidor
HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 12347        # Porta do servidor
BUFFER_SIZE = 1024  # Tamanho do buffer
TIMEOUT = 2         # Tempo de timeout em segundos

# Criando o socket UDP para enviar
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Associando o socket ao endereço e porta
udp_socket.bind((HOST, PORT))

# Criando o socket UDP para receber ACKs
recv_ACK_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Associando o socket de receber ACK ao endereço e porta
recv_ACK_socket.bind((HOST, PORT+1))

def receber_ack():
    while True:
        recv_ACK_socket.settimeout(TIMEOUT)
        try: 
            ack, _ = recv_ACK_socket.recvfrom(BUFFER_SIZE)
            if ack.decode() == "ACK":
                print('Recebi o ACK')
                return True
        except socket.timeout:
            return False

num_salas = 5
nome_salas = ["E101", "E102","E103", "E104", "E105"]
num_dias = 5
nome_dias = ["seg", "ter", "qua", "qui", "sex"]
num_horarios = 9
nome_horarios = ["08h", "09h", "10h", "11h", "12h", "13h", "14h", "15h", "16h"]

# Inicializando a matriz com valores padrão (por exemplo, "vazia")
matriz_ocupacao = [[[None for _ in range(num_horarios)] for _ in range(num_dias)] for _ in range(num_salas)]

# Função para visualizar a matriz de ocupação
def visualizar_matriz(matriz):
    for dia in range(num_dias):
        print(f"Dia: {nome_dias[dia]}:")
        for sala in range(num_salas):
            for horario in range(num_horarios):
                ocupante = matriz[sala][dia][horario]
                print(f"Sala: {nome_salas[sala]}, Horário {nome_horarios[horario]}: {ocupante if ocupante else 'Vazia'}")
    print("\n")

lista_usuarios = []


print('Servidor UDP pronto para receber arquivos...')
while True:
    data, addr = udp_socket.recvfrom(BUFFER_SIZE) # recebendo o dado e endereço do cliente que enviou
    addrACK = (addr[0],(addr[1]+1))
    udp_socket.sendto("ACK".encode(), addrACK)       # Enviar ACK para o cliente
    print(f'Enviando ACK para {addrACK}')
    
    frase = []
    frase = data.decode()                         # Hora - 3 char, dia - 3 char, sala - 4char
    frase = frase.strip()
    frase = frase.split(' ')
    print(frase)
    
    match frase[0].lower():
        case 'connect':
            if frase[2] and frase[3]:

                nome_completo = f'{frase[2]} {frase[3]}'
                print(f'Chegou mais 1 usuário: {nome_completo} no IP: {addr}')
                mensagem_conexao = 'Você se conectou!'
                lista_usuarios.append((nome_completo, addr))

                for _ in range(100):  
                    udp_socket.sendto(mensagem_conexao.encode(), addr)
                    if receber_ack():
                        break

                # Enviar mensagem para todos os outros clientes
                for tupla in lista_usuarios:
                    if tupla[1] != addr:
                        mensagem = f'{nome_completo} acabou de se conectar ao servidor'
                        for _ in range(100):  
                            udp_socket.sendto(mensagem.encode(), tupla[1])
                            if receber_ack():
                                break

            else:
                mensagem_erro = 'O comando connect precisa ter um nome composto de 2 palavras. Ex: \'connect as Pedro Miguel\''
                for _ in range(100):  
                    udp_socket.sendto(mensagem_erro.encode(), addr)
                    if receber_ack():
                        break

        case 'bye':
            menssagem = 'Thau'
            for tupla in lista_usuarios[:]:  # Usando uma cópia da lista para evitar problemas de iteração
                if addr in tupla:
                    lista_usuarios.remove(tupla)
                    nome_completo = tupla[0]
                    print(f"Adeus Imundice {tupla[0]}")
            for _ in range(100):  
                    udp_socket.sendto(menssagem.encode(), addr)
                    if receber_ack():
                        break
            # Enviar mensagem para todos os outros clientes
            for tupla in lista_usuarios:
                if tupla[1] != addr:
                    mensagem = f'{nome_completo} acabou de se desconectar do servidor'
                    for _ in range(100):  
                        udp_socket.sendto(mensagem.encode(), tupla[1])
                        if receber_ack():
                            break

        case 'list':
            print("Toma a lista")
            menssagem = f'A lista : {lista_usuarios}'
            for _ in range(100):  
                udp_socket.sendto(menssagem.encode(), addr)
                if receber_ack():
                    break

        case 'reservar':
            flag = 0
            if (frase[1] != None and frase[2] != None and frase[3] != None and frase[1] in nome_salas and frase[2] in nome_dias and frase[3] in nome_horarios):
                for tupla in lista_usuarios[:]:  # Usando uma cópia da lista para evitar problemas de iteração
                    if addr in tupla:
                        nome_completo = tupla[0]
                        flag = 1
                        salaDesejada = nome_salas.index(frase[1].upper())
                        diaDesejado = nome_dias.index(frase[2].lower())
                        horarioDesejado = nome_horarios.index(frase[3].lower())
                        if matriz_ocupacao[salaDesejada][diaDesejado][horarioDesejado] == None:
                            menssagem = 'Sala Reservada'
                            for _ in range(100):  
                                udp_socket.sendto(menssagem.encode(), addr)
                                if receber_ack():
                                    break
                            matriz_ocupacao[salaDesejada][diaDesejado][horarioDesejado] = tupla
                            # Enviar mensagem para todos os outros clientes
                            for tuplas in lista_usuarios:
                                if tuplas[1] != addr:
                                    mensagem = f'{nome_completo} acabou de reservar a sala: {frase[1]} no dia {frase[2]} as {frase[3]}'
                                    for _ in range(100):  
                                        udp_socket.sendto(mensagem.encode(), tuplas[1])
                                        if receber_ack():
                                            break
                        else:
                            menssagem = f'Essa sala já foi reservada por {(matriz_ocupacao[salaDesejada][diaDesejado][horarioDesejado])[0]}'
                            for _ in range(100):  
                                        udp_socket.sendto(menssagem.encode(), addr)
                                        if receber_ack():
                                            break
            
                            
                if flag == 0:   
                    menssagem = 'Você não está conectado'
                    for _ in range(100):  
                        udp_socket.sendto(menssagem.encode(), addr)
                        if receber_ack():
                            break
            else:
                menssagem = 'Comando errado'
                for _ in range(100):  
                    udp_socket.sendto(menssagem.encode(), addr)
                    if receber_ack():
                        break

        case 'cancelar':
            flag = 0
            if frase[1] != None and frase[2] != None and frase[3] != None  and frase[1] in nome_salas and frase[2] in nome_dias and frase[3] in nome_horarios:
                for tupla in lista_usuarios[:]:  
                    if addr in tupla:
                        flag = 1
                        nome_completo = tupla[0]
                        salaDesejada = nome_salas.index(frase[1].upper())
                        diaDesejado = nome_dias.index(frase[2].lower())
                        horarioDesejado = nome_horarios.index(frase[3].lower())
                        if matriz_ocupacao[salaDesejada][diaDesejado][horarioDesejado] == tupla:
                            menssagem = 'Reserva cancelada'
                            for _ in range(100):  
                                udp_socket.sendto(menssagem.encode(), addr)
                                if receber_ack():
                                    break
                            matriz_ocupacao[salaDesejada][diaDesejado][horarioDesejado] = None
                            for tuplas in lista_usuarios:
                                if tuplas[1] != addr:
                                    mensagem = f'{nome_completo} acabou de cancelar a reserva da sala: {frase[1]} no dia {frase[2]} as {frase[3]}'
                                    for _ in range(100):  
                                        udp_socket.sendto(mensagem.encode(), tuplas[1])
                                        if receber_ack():
                                            break
                        else:
                            menssagem = f'Você não reservou essa sala!'
                            for _ in range(100):  
                                udp_socket.sendto(menssagem.encode(), addr)
                                if receber_ack():
                                    break
                            
                if flag == 0:   
                    menssagem = 'Você não está conectado'
                    for _ in range(100):  
                        udp_socket.sendto(menssagem.encode(), addr)
                        if receber_ack():
                            break
                    udp_socket.sendto(menssagem.encode(), addr)
            else:
                menssagem = 'Comando errado'
                for _ in range(100):  
                    udp_socket.sendto(menssagem.encode(), addr)
                    if receber_ack():
                        break
                    
        case 'check':
            lista_disponivel = []
            flag = 0
            if frase[1] != None and frase[2] != None and frase[1] in nome_salas and frase[2] in nome_dias:
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
                    for _ in range(100):  
                        udp_socket.sendto(menssagem.encode(), addr)
                        if receber_ack():
                            break
                    
                if lista_disponivel == [] and flag == 1:
                    menssagem = 'Não há horários disponíveis'
                    for _ in range(100):  
                        udp_socket.sendto(menssagem.encode(), addr)
                        if receber_ack():
                            break 

                if lista_disponivel != []:
                    menssagem = f'{lista_disponivel}'
                    for _ in range(100):  
                        udp_socket.sendto(menssagem.encode(), addr)
                        if receber_ack():
                            break
            else:
                menssagem = 'Comando errado'
                for _ in range(100):  
                    udp_socket.sendto(menssagem.encode(), addr)
                    if receber_ack():
                        break         
        case _ :
            print ("Comando errado")
            menssagem = 'Comando errado'
            for _ in range(100):  
                udp_socket.sendto(menssagem.encode(), addr)
                if receber_ack():
                    break
            



