
import platform
import socket
import threading
import requests
import time
import subprocess
import os
import platform

HOST='localhost'
PORT=65000
BUFFER_SIZE=256
CODE_PAGE='utf-8'

TELEGRAM_API_URL ="https://api.telegram.org/bot6958977609:AAE5X1-eA9spI7dXOfal1g7WWytgwWmvXeU"
#"https://api.telegram.org/bot6788315183:AAG6g041wJ2RmHX_1WHrqrzjcOyIhkCO5II"
TELEGRAM_CHAT_ID = "6440731935"
#"6440731935"

tcp_socket = None

def get_platform():
    return platform.system().lower()

def handle_client(connection,address):
    print(f"conexão estabelecida com {address}")

    try:
        while True:
            data = connection.recv(BUFFER_SIZE)
            if not data:
                print(f"conexão encerrada por{address}")
                break

            message = data.decode(CODE_PAGE)
            print(f"mensagem recebida de {address}:{message}")

            response =processar_mensagem(message)

            connection.sendall(response.encode(CODE_PAGE))

    except ConnectionResetError:
        print(f"conexao redefinida")
    except Exception as e:
        print(f"erro  com a conexao:{str(e)}")

    finally:
        connection.close()
        print(f"conexão fechada por {address}")

def start_server():
    global tcp_socket
    tcp_socket =socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        tcp_socket.bind((HOST,PORT))
        tcp_socket.listen()

        print(f'Aguardando conexões em{HOST}:{PORT}\n')

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
        print(f"erro ao iniciar o servidor:{str(e)}")
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
        return verificar_resposta_ip()
    elif msg.startswith('/service '):
        return verificar_servico()
    elif msg.lower() == '/dns':
        return obter_informacoes_dns()
    elif msg.lower() == '/map':
        return obter_mapa_de_rede()
    else:
        return "comando nao reconhecido"

def obter_informacoes_de_rede():
    try:
        if get_platform() =='windows':
            endereco_ip =os.popen("ipconfig  | findstr \"Endereço IPv4\"").read().split(':')[-1].strip()
            gateway =os.popen("ipconfig | findstr \"Default Gateway\"").read().split(':')[-1].strip()
        else:
            #endereco_ip = subprocess.check_output(['hostname', '-I']).decode(CODE_PAGE).strip()
            endereco_ip=os.popen('hostname -I').read().strip().split()[0]
            gateway = subprocess.check_output(['ip', 'route', 'show', 'default']).decode(CODE_PAGE).split(' ')[2].strip()

        mascara_subrede ='255.255.255.0'
        return f"informações básicas sobre a rede:\nIP:{endereco_ip}\nMáscara: {mascara_subrede}\nGateway: {gateway}"
    except Exception as e:
        return f"erro ao obter informações de rede:{str(e)}"

def ping_google():
    try:
        if get_platform() =='windows':
            resultado = subprocess.run(['ping', '-n', '4', 'google.com'],capture_output=True,text=True).stdout
        else:
            resultado = subprocess.run(['ping', '-c', '4', 'google.com'],capture_output=True,text=True).stdout
        return resultado
    except Exception as e:
        return f"erro ao executar o comando ping: {str(e)}"





def verificar_resposta_ip(endereco_ip):
    try:
        if get_platform() == 'windows':
            resultado = subprocess.run(['ping', '-n', '4', endereco_ip],capture_output=True,text=True,check=True)
        else:
            resultado = subprocess.run(['ping', '-c', '4', endereco_ip],capture_output=True,text=True,check=True)

        return resultado.stdout
    except subprocess.CalledProcessError as e:
        return f"erro ao verificar a resposta do ip {endereco_ip}:O comando ping retornou um código de erro. Saída do subprocesso: {e.output}"
    except Exception as e:
        return f"erro ao verificar a resposta do ip {endereco_ip}:{str(e)}"




def verificar_servico():
    try:
        ip = 'localhost' 
        port = 65000  
        if get_platform() =='windows':
            resultado =subprocess.run(['Test-NetConnection', '-ComputerName', ip, '-Port', str(port)],capture_output=True,text=True).stdout
        else:
            resultado =subprocess.run(['nc', '-zv', ip, str(port)],capture_output=True,text=True).stdout
        return resultado
    except Exception as e:
        return f"erro ao verificar o serviço em {ip}:{port}: {str(e)}"

    


def obter_informacoes_dns():
    try:
        if get_platform() =='windows':
            resultado =subprocess.run(['nslookup', 'google.com'], capture_output=True,text=True).stdout
        else:
            resultado =subprocess.run(['host', 'google.com'], capture_output=True,text=True).stdout
        return resultado
    except Exception as e:
        return f"rro ao obter informacoes de dns: {str(e)}"
    



def obter_mapa_de_rede():
    try:
        if get_platform() =='windows':
            resultado =subprocess.run(['arp', '-a'], capture_output=True, text=True).stdout
        else:
            resultado =subprocess.run(['arp', '-n'], capture_output=True, text=True).stdout
        return resultado
    except Exception as e:
        return f"erro ao obter o mapa de rede: {str(e)}"
  

def verificar_novas_mensagens():
    offset=None

    while True:
        try:
            url =f"{TELEGRAM_API_URL}/getUpdates?offset={offset}"
            response = requests.get(url)
            data = response.json()

            if "result" in data and data["result"]:
                for update in data["result"]:
                    offset =update["update_id"] + 1
                    processar_mensagem_telegram(update["message"]["text"],update["message"]["chat"]["id"])

            time.sleep(1)  

        except Exception as e:
            print(f"Erro ao verificar novas mensagens do Telegram: {str(e)}")
            time.sleep(5) 

def processar_mensagem_telegram(texto,chat_id):
    response = processar_mensagem(texto)
    enviar_resposta_telegram(response,chat_id)

def enviar_resposta_telegram(texto,chat_id):
    try:
        url = f"{TELEGRAM_API_URL}/sendMessage"
        params={"chat_id": chat_id, "text": texto}
        requests.get(url, params=params)
    except Exception as e:
        print(f"Erro ao enviar resposta ao Telegram: {str(e)}")

if __name__=="__main__":
    # Inicie o servidor em uma thread separada
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    # Inicie o loop para verificar novas mensagens do Telegram em outra thread separada
    telegram_thread=threading.Thread(target=verificar_novas_mensagens)
    telegram_thread.start()
