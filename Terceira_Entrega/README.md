# Gerenciamento de Reservas - Terceira Etapa

Esta é a terceira esntrega do projeto relativo a cadeira de INFRA-ESTRUTURA DE COMUNICACAO 2023.2 

## Objetivo da Entrega

Implementação do sistema de reservas, exibido por linha de comando. Apesar do reaproveitamento das etapas anteriores, o histórico da execução dos algoritmos não deve ser exibido nessa etapa, apenas a aplicação como descrita nesse documento e mantendo o uso do rdt3.0.

## Como Executar

1. Certifique-se de ter o Python instalado em sua máquina.

2. Abra ao menos três terminais, um para o servidor e os demais para os clientes.

3. Para terminais Linux:

- No terminal do servidor, navegue até a pasta onde está localizado o arquivo servidor.py e execute o comando:

python3 servidor.py


- No terminal do cliente, navegue até a pasta onde está localizado o arquivo cliente.py e execute o comando:

python3 cliente.py

4. VS code: 

- Apenas execute primeiro o terminal do servidor e em seguida os dos clientes.

Funcionalidade                                      Comando

Conectar ao aplicativo                              connect as <nome_do_usuario>

Sair do aplicativo                                  bye

Exibir lista de usuários conectados no momento      list

Reservar uma sala                                   reservar <numero_da_sala> <dia> <horário>

Cancelar uma reserva                                cancelar <numero_da_sala> <dia> <horário>

Verificar disponibilidade em sala específica        check <numero_da_sala> <dia>



## Notas Adicionais

Lembrando que a maior parte dos comandos demanda que o cliente esteja conectado.