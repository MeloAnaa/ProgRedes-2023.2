

#servidor.py
import socket
import threading
from ex_cliente import processar_mensagem

HOST = 'localhost'
PORT = 65000
BUFFER_SIZE = 256
CODE_PAGE = 'utf-8'

TELEGRAM_API_URL = "https://api.telegram.org/bot6958977609:AAE5X1-eA9spI7dXOfal1g7WWytgwWmvXeU"
#"https://api.telegram.org/bot6940628899:AAGh8IdmgHkFl8dZlMTCFKikWiJ39KiwVQI"

TELEGRAM_CHAT_ID = "6440731935"





def handle_client(connection, address):
    print(f"conexão estabelecida com {address}")

    try:
        while True:
            data = connection.recv(BUFFER_SIZE)
            if not data:
                print(f"conexão encerrada por {address}")
                break

            message = data.decode(CODE_PAGE)
            print(f"mensagem recebida de: {address}: {message}")

            response = processar_mensagem(message)

            connection.sendall(response.encode(CODE_PAGE))

    except ConnectionResetError:
        print(f"conexão redefinida por {address}")
    except Exception as e:
        print(f"erro ao lidar com a conexão: {str(e)}")

    finally:
        connection.close()
        print(f"conexão fechada por {address}")





def start_server():

    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        tcp_socket.bind((HOST, PORT))
        tcp_socket.listen()

        print(f'aguardando conexões em{HOST}:{PORT}\n')

        while True:
            client_connection, client_address=tcp_socket.accept()
            ip_cliente, porta_cliente=client_address
            print(f'{ip_cliente} conectado na porta{porta_cliente}')

            client_thread =threading.Thread(
                target=handle_client,
                args=(client_connection,client_address)
            )

            client_thread.start()

    except Exception as e:
        print(f"erro ao iniciar o servidor:{str(e)}")
    finally:
        tcp_socket.close()



if __name__== '__main__':
    start_server() 



