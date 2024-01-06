


# servidor.py
import socket
import threading
import requests
import time
import subprocess
import os
import re

HOST = 'localhost'
PORT = 65000
BUFFER_SIZE = 256
CODE_PAGE = 'utf-8'

TELEGRAM_API_URL = "https://api.telegram.org/bot6788315183:AAG6g041wJ2RmHX_1WHrqrzjcOyIhkCO5II"
TELEGRAM_CHAT_ID = "6440731935"

tcp_socket = None

def handle_client(connection, address):
    print(f"Conexão estabelecida com {address}")

    try:
        while True:
            data = connection.recv(BUFFER_SIZE)
            if not data:
                print(f"Conexão encerrada por {address}")
                break

            message = data.decode(CODE_PAGE)
            print(f"Mensagem recebida de {address}: {message}")

            # Processar mensagem e obter resposta
            response = processar_mensagem(message)

            # Enviar resposta de volta ao cliente
            connection.sendall(response.encode(CODE_PAGE))

    except ConnectionResetError:
        print(f"Conexão redefinida por {address}")
    except Exception as e:
        print(f"Erro ao lidar com a conexão: {str(e)}")

    finally:
        connection.close()
        print(f"Conexão fechada por {address}")

def start_server():
    global tcp_socket
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        tcp_socket.bind((HOST, PORT))
        tcp_socket.listen()

        print(f'Aguardando conexões em {HOST}:{PORT}\n')

        while True:
            client_connection, client_address = tcp_socket.accept()
            ip_cliente, porta_cliente = client_address
            print(f'{ip_cliente} conectado na porta {porta_cliente}')

            client_thread = threading.Thread(
                target=handle_client,
                args=(client_connection, client_address)
            )

            client_thread.start()

    except Exception as e:
        print(f"Erro ao iniciar o servidor: {str(e)}")
    finally:
        tcp_socket.close()

def processar_mensagem(msg):
    if msg.lower() == '/ola':
        return "Olá, meu amigo!"
    elif msg.lower() == '/info':
        return obter_informacoes_de_rede()
    elif msg.lower() == '/ping':
        return ping_google()
    elif msg.startswith('/active '):
        return verificar_resposta_ip(msg.split()[1])
    elif msg.startswith('/service '):
        return verificar_servico(msg.split()[1])
    elif msg.lower() == '/dns':
        return obter_informacoes_dns()
    elif msg.lower() == '/map':
        return obter_mapa_de_rede()
    else:
        return "Comando não reconhecido!"

def obter_informacoes_de_rede():
    try:
        #endereco_ip = os.popen('ipconfig').read().split('\n')[1].split(':')[-1].strip()
        endereco_ip = os.popen("ipconfig  | findstr \"Endereço IPv4\"").read().split(':')[-1].strip()
       
        mascara_subrede = '255.255.255.0'
        gateway = os.popen("ipconfig | findstr \"Default Gateway\"").read().split(':')[-1].strip()
        return f"Informações básicas sobre a rede:\nIP: {endereco_ip}\nMáscara: {mascara_subrede}\nGateway: {gateway}"
    except Exception as e:
        return f"Erro ao obter informações de rede: {str(e)}"




def ping_google():
    try:
        resultado = subprocess.run(['ping', '-n', '4', 'google.com'], capture_output=True, text=True).stdout
        return resultado
    except Exception as e:
        return f"Erro ao executar o comando ping: {str(e)}"

def verificar_resposta_ip(endereco_ip):
    try:
        resultado = subprocess.run(['ping', '-n', '4', endereco_ip], capture_output=True, text=True).stdout
        return resultado
    except Exception as e:
        return f"Erro ao verificar a resposta do IP {endereco_ip}: {str(e)}"

def verificar_servico(ip_and_port):
    try:
        ip, port = ip_and_port.split(':')
        resultado = subprocess.run(['Test-NetConnection', '-ComputerName', ip, '-Port', port], capture_output=True, text=True).stdout
        return resultado
    except Exception as e:
        return f"Erro ao verificar o serviço em {ip_and_port}: {str(e)}"

def obter_informacoes_dns():
    try:
        resultado = subprocess.run(['nslookup', 'google.com'], capture_output=True, text=True).stdout
        return resultado
    except Exception as e:
        return f"Erro ao obter informações de DNS: {str(e)}"

def obter_mapa_de_rede():
    try:
        resultado = subprocess.run(['arp', '-a'], capture_output=True, text=True).stdout
        return resultado
    except Exception as e:
        return f"Erro ao obter o mapa de rede: {str(e)}"

def verificar_novas_mensagens():
    offset = None

    while True:
        try:
            url = f"{TELEGRAM_API_URL}/getUpdates?offset={offset}"
            response = requests.get(url)
            data = response.json()

            if "result" in data and data["result"]:
                for update in data["result"]:
                    offset = update["update_id"] + 1
                    processar_mensagem_telegram(update["message"]["text"], update["message"]["chat"]["id"])

            time.sleep(1)  # Aguarda 1 segundo antes de verificar novamente

        except Exception as e:
            print(f"Erro ao verificar novas mensagens do Telegram: {str(e)}")
            time.sleep(5)  # Em caso de erro, aguarda 5 segundos antes de tentar novamente

def processar_mensagem_telegram(texto, chat_id):
    response = processar_mensagem(texto)
    enviar_resposta_telegram(response, chat_id)

def enviar_resposta_telegram(texto, chat_id):
    try:
        url = f"{TELEGRAM_API_URL}/sendMessage"
        params = {"chat_id": chat_id, "text": texto}
        requests.get(url, params=params)
    except Exception as e:
        print(f"Erro ao enviar resposta ao Telegram: {str(e)}")

if __name__ == "__main__":
    # Inicie o servidor em uma thread separada
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    # Inicie o loop para verificar novas mensagens do Telegram em outra thread separada
    telegram_thread = threading.Thread(target=verificar_novas_mensagens)
    telegram_thread.start()


