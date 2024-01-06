
#cliente.py

import socket
import time
HOST        = 'localhost'
PORT        = 65000       
BUFFER_SIZE = 256         
CODE_PAGE   = 'utf-8'     


tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


tentativas = 0

while True:
    try:
        tcp_socket.connect((HOST, PORT))

        print('Conexão estabelecida.')
        print()
        
        msg = input('Digite a mensagem: ')
        print('')
        if msg:
            msg = msg.encode(CODE_PAGE)
            tcp_socket.send(msg)

            data_retorno = tcp_socket.recv(BUFFER_SIZE)
            msg_retorno = data_retorno.decode(CODE_PAGE)
            print(f'Servidor diz: {msg_retorno}')

    except (socket.error, ConnectionError):
        # Lidar com a desconexão
        print('Tentando conectar...')
        time.sleep(5)
        tentativas += 1
        print(f"Tentativa de conexão: {tentativas}")

        # Recriar o socket
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  
