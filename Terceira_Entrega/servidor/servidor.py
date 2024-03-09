import socket

# Configurações do servidor
HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 12347        # Porta do servidor
BUFFER_SIZE = 1024  # Tamanho do buffer
TIMEOUT = 2         # Tempo de timeout em segundos

# Criando o socket UDP
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Associando o socket ao endereço e porta
udp_socket.bind((HOST, PORT))

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
    frase = data.decode()                         # Hora - 3 char, dia - 3 char, sala - 4char
    frase = frase.strip()
    frase = frase.split(' ')
    print(frase)
    
    match frase[0].lower():
        case 'connect':
            print(f'Chegou mais 1 corno: {frase[2]} no IP: {addr}')       # addr = Ip server + porta cliente (unico)
            menssagem = f'{frase[2]} se conectou'
            lista_usuarios.append((frase[2] + ' ' + frase[3], addr )) 
            udp_socket.sendto(menssagem.encode(), addr)

        case 'bye':
            print("Adeus Imundice")
            menssagem = 'Thau'
            for tupla in lista_usuarios[:]:  # Usando uma cópia da lista para evitar problemas de iteração
                if addr in tupla:
                    lista_usuarios.remove(tupla)
            udp_socket.sendto(menssagem.encode(), addr)

        case 'list':
            print("Toma a lista")
            menssagem = f'A lista : {lista_usuarios}'
            udp_socket.sendto(menssagem.encode(), addr)

        case 'reservar':
            flag = 0
            if frase[1] != None and frase[2] != None and frase[3] != None:
                for tupla in lista_usuarios[:]:  # Usando uma cópia da lista para evitar problemas de iteração
                    if addr in tupla:
                        flag = 1
                        salaDesejada = nome_salas.index(frase[1].upper	())
                        diaDesejado = nome_dias.index(frase[2].lower())
                        horarioDesejado = nome_horarios.index(frase[3].lower())
                        if matriz_ocupacao[salaDesejada][diaDesejado][horarioDesejado] == None:
                            menssagem = 'Sala Reservada'
                            udp_socket.sendto(menssagem.encode(), addr)
                            matriz_ocupacao[salaDesejada][diaDesejado][horarioDesejado] = tupla
                        else:
                            menssagem = f'Essa sala já foi reservada por {(matriz_ocupacao[salaDesejada][diaDesejado][horarioDesejado])[0]}'
                            udp_socket.sendto(menssagem.encode(), addr)
            
                            
                if flag == 0:   
                    menssagem = 'Você não está conectado'
                    udp_socket.sendto(menssagem.encode(), addr)
            else:
                menssagem = 'Comando errado'
                udp_socket.sendto(menssagem.encode(), addr) 

        case 'cancelar':
            flag = 0
            if frase[1] != None and frase[2] != None and frase[3] != None:
                for tupla in lista_usuarios[:]:  
                    if addr in tupla:
                        flag = 1
                        salaDesejada = nome_salas.index(frase[1])
                        diaDesejado = nome_dias.index(frase[2])
                        horarioDesejado = nome_horarios.index(frase[3])
                        if matriz_ocupacao[salaDesejada][diaDesejado][horarioDesejado] == tupla:
                            menssagem = 'Reserva cancelada'
                            udp_socket.sendto(menssagem.encode(), addr)
                            matriz_ocupacao[salaDesejada][diaDesejado][horarioDesejado] = None
                        else:
                            menssagem = f'Você não reservou essa sala!'
                            udp_socket.sendto(menssagem.encode(), addr)
        
                if flag == 0:   
                    menssagem = 'Você não está conectado'
                    udp_socket.sendto(menssagem.encode(), addr)
            else:
                menssagem = 'Comando errado'
                udp_socket.sendto(menssagem.encode(), addr)  
            
        case 'check':
            lista_disponivel = []
            flag = 0
            if frase[1] != None and frase[2] != None:
                for tupla in lista_usuarios[:]:  
                    if addr in tupla:
                        flag = 1
                        salaDesejada = nome_salas.index(frase[1])
                        diaDesejado = nome_dias.index(frase[2])
                        for i in range(num_horarios):
                            if matriz_ocupacao[salaDesejada][diaDesejado][i] == None:
                                lista_disponivel.append(nome_horarios[i])
                 
                if flag == 0:   
                    menssagem = 'Você não está conectado'
                    udp_socket.sendto(menssagem.encode(), addr)
            
                if lista_disponivel == [] and flag == 1:
                    menssagem = 'Não há horários disponíveis'
                    udp_socket.sendto(menssagem.encode(), addr)    

                if lista_disponivel != []:
                    menssagem = f'{lista_disponivel}'
                    udp_socket.sendto(menssagem.encode(), addr)
            else:
                menssagem = 'Comando errado'
                udp_socket.sendto(menssagem.encode(), addr)          
        case _ :
            print ("Comando errado")
            menssagem = 'Comando errado'
            udp_socket.sendto(menssagem.encode(), addr)



