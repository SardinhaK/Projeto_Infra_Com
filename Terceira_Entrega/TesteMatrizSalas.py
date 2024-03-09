# Definindo as dimensões da matriz
num_salas = 5
nome_salas = ["E101", "E102","E103", "E104", "E105"]
num_dias = 5
nome_dias = ["Seg", "Ter", "Qua", "Qui", "Sex"]
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
    