# Gerenciamento de Reservas - Primeira Etapa

Este é o projeto da primeira etapa, que consiste na implementação de uma ferramenta de transferência de arquivos usando comunicação UDP.

## Objetivo da Entrega

O objetivo desta entrega é desenvolver um sistema de transferência de arquivos entre um cliente e um servidor, utilizando UDP. O cliente deve enviar solicitações para arquivos específicos ao servidor, que por sua vez os envia de volta para o cliente.

## Como Executar

1. Certifique-se de ter o Python instalado em sua máquina.

2. Abra dois terminais, um para o cliente e outro para o servidor.

3. No terminal do servidor, navegue até a pasta onde está localizado o arquivo `servidor.py` e execute o comando:

python servidor.py


4. No terminal do cliente, navegue até a pasta onde está localizado o arquivo `cliente.py` e execute o comando:


5. Verifique na pasta do cliente se os arquivos solicitados foram recebidos com sucesso.

## Notas Adicionais

- Certifique-se de ter pelo menos dois arquivos diferentes na pasta do servidor para testar a transferência de arquivos.
- O servidor utiliza a porta 12345 e o cliente utiliza a porta 12346 para comunicação.
