# Gerenciamento de Reservas - Segunda Etapa

Este é o projeto da segunda etapa, que consiste na implementação de uma transferência confiável com RDT 3.0

## Objetivo da Entrega

O objetivo desta entrega é desenvolver a segunda etapa do sistema de transferência de arquivos confiável entre um cliente e um servidor, utilizando UDP. Nesta etapa, implementaremos o canal de transmissão confiável RDT 3.0, conforme apresentado na disciplina e descrito no livro-texto de Kurose. A cada passo executado do algoritmo, em tempo de execução, será impresso na linha de comando para proporcionar uma compreensão detalhada do que está acontecendo. Além disso, para testar o algoritmo, será implementado um gerador de perdas de pacotes aleatórios, causando timeouts no transmissor para esses pacotes, a fim de demonstrar a eficiência do RDT 3.0 implementado.

## Como Executar

1. Certifique-se de ter o Python instalado em sua máquina.

2. Abra dois terminais, um para o cliente e outro para o servidor.

3. No terminal do servidor, navegue até a pasta onde está localizado o arquivo `servidor.py` e execute o comando:

python3 servidor.py


4. No terminal do cliente, navegue até a pasta onde está localizado o arquivo `cliente.py` e execute o comando:

python3 cliente.py

5. Verifique na pasta do cliente se os arquivos solicitados foram recebidos com sucesso.

## Notas Adicionais

- Certifique-se de ter pelo menos dois arquivos diferentes na pasta do servidor nomeados como e 'mensagem.txt' e 'imagem.jpeg' para testar a transferência de arquivos.
- O servidor utiliza a porta 12347 e o cliente utiliza a porta 12348 para comunicação.
