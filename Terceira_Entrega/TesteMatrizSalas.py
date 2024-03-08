# Definindo as dimensões da matriz
num_salas = 5
nome_salas = ["E101", "E102","E103", "E104", "E105"]
num_dias = 5
nome_dias = ["Seg", "Ter", "Qua", "Qui", "Sex"]
num_horarios = 9

# Inicializando a matriz com valores padrão (por exemplo, "vazia")
matriz_ocupacao = [[[None for _ in range(num_horarios)] for _ in range(num_dias)] for _ in range(num_salas)]

# Função para visualizar a matriz de ocupação
def visualizar_matriz(matriz):
    for dia in range(num_dias):
        print(f"Dia: {nome_dias[dia]}:")
        for sala in range(num_salas):
            for horario in range(num_horarios):
                ocupante = matriz[sala][dia][horario]
                print(f"Sala: {nome_salas[sala]}, Horário {horario + 8}: {ocupante if ocupante else 'Vazia'}")
    print("\n")

# Exemplo de utilização:
# Marcar que a Sala 3 está ocupada na segunda-feira (Dia 2), Horário 4
matriz_ocupacao[2][1][3] = "João"

# Marcar que a Sala 1 está ocupada na quarta-feira (Dia 4), Horário 7
matriz_ocupacao[0][3][6] = "Maria"

# Visualizar a matriz de ocupação
visualizar_matriz(matriz_ocupacao)
