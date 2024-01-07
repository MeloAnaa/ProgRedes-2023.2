

#cliente.py

import socket
import platform
import threading
#import funcoes_bot
import requests
import time
import os
import psutil
import subprocess 
from datetime import datetime
HOST        = 'localhost'
PORT        = 65000       
BUFFER_SIZE = 256         
CODE_PAGE   = 'utf-8'     
TELEGRAM_API_URL = "https://api.telegram.org/bot6958977609:AAE5X1-eA9spI7dXOfal1g7WWytgwWmvXeU"
TELEGRAM_CHAT_ID = "6440731935"


tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


tentativas = 0

def obter_nome_sistema():
    return platform.system().lower()


def obter_informacoes_de_maquina():
    uname = platform.uname()
    info = f"System: {uname.system}\n"
    info += f"Node Name: {uname.node}\n"
    info += f"Release: {uname.release}\n"
    info += f"Version: {uname.version}\n"
    info += f"Machine: {uname.machine}\n"
    info += f"Processor: {uname.processor}"

    return info

def obter_programas_instalados():
    uname = platform.uname()
    if uname.system == 'windows':
        Data = subprocess.check_output(['wmic', 'product', 'get', 'name']) 
        a = str(Data) 
        programas = ''
        try: 
            
            for i in range(len(a)): 
                programas += a.split("\\r\\r\\n")[6:][i]
            return programas
        except IndexError as e: 
            print("All Done")
    return 'No data found.'    

def obter_informacoes_de_rede():
    try:
        if obter_nome_sistema()=='windows':
            endereco_ip=os.popen("ipconfig  | findstr \"Endereço IPv4\"").read().split(':')[-1].strip()
            gateway=os.popen("ipconfig | findstr \"Default Gateway\"").read().split(':')[-1].strip()
        else:
            #endereco_ip = subprocess.check_output(['hostname', '-I']).decode(CODE_PAGE).strip()
            endereco_ip=os.popen('hostname -I').read().strip().split()[0]
            gateway = subprocess.check_output(['ip', 'route', 'show', 'default']).decode(CODE_PAGE).split(' ')[2].strip()

        mascara_subrede = '255.255.255.0'
        return f"informações basicas sobre a rede:\nIP: {endereco_ip}\nmáscara: {mascara_subrede}\ngateway: {gateway}"
    except Exception as e:
        return f"erro ao obter informacoes de rede: {str(e)}"

def ping_google():
    try:
        if obter_nome_sistema()=='windows':
            resultado = subprocess.run(['ping', '-n', '4', 'google.com'],capture_output=True,text=True).stdout
        else:
            resultado = subprocess.run(['ping', '-c', '4', 'google.com'],capture_output=True,text=True).stdout
        return resultado
    except Exception as e:
        return f"erro ao executar o comando ping: {str(e)}"

def verificar_resposta_ip(endereco_ip):
    try:
        if obter_nome_sistema()== 'windows':
            resultado=subprocess.run(['ping', '-n', '4', endereco_ip],capture_output=True,text=True,check=True)
        else:
            resultado=subprocess.run(['ping', '-c', '4', endereco_ip],capture_output=True, text=True,check=True)

        return resultado.stdout
    except subprocess.CalledProcessError as e:
        return f"erro ao verificar a resposta do ip: {endereco_ip}: O ping retornou um erro. Saída do subprocesso:{e.output}"
    except Exception as e:
        return f"erro ao verificar a resposta do ip: {endereco_ip}: {str(e)}"

def verificar_servico():
    try:
        ip='localhost' 
        port=65000  
        if obter_nome_sistema()== 'windows':
            resultado = subprocess.run(['Test-NetConnection', '-ComputerName', ip, '-Port', str(port)], capture_output=True, text=True).stdout
        else:
            resultado = subprocess.run(['nc', '-zv', ip, str(port)], capture_output=True, text=True).stdout
        return resultado
    except Exception as e:
        return f"erro ao verificar o serviço em {ip}:{port}: {str(e)}"

def obter_informacoes_dns():
    try:
        if obter_nome_sistema() =='windows':
            resultado = subprocess.run(['nslookup', 'google.com'], capture_output=True, text=True).stdout
        else:
            resultado = subprocess.run(['host', 'google.com'], capture_output=True, text=True).stdout
        return resultado
    except Exception as e:
        return f"erro ao obter informacoes de DNS: {str(e)}"
    
def obter_mapa_de_rede():
    try:
        if obter_nome_sistema() =='windows':
            resultado = subprocess.run(['arp', '-a'],capture_output=True,text=True).stdout
        else:
            resultado = subprocess.run(['arp', '-n'],capture_output=True,text=True).stdout
        return resultado
    except Exception as e:
        return f"erro ao obter o mapa de rede:{str(e)}"
  
def processar_mensagem(msg):
    if msg.lower() == '/ola':
        return "Olá, meu amigo!"
    elif msg.lower() == '/info':
        return obter_informacoes_de_rede()
    elif msg.lower() == '/hardware':
        return obter_informacoes_de_maquina()
    elif msg.lower() == '/programas':
        return obter_programas_instalados()    
    elif msg.lower() == '/ping':
        return ping_google()
    elif msg.lower() == '/active':
        return verificar_resposta_ip()
    elif msg.lower() == '/service':
        return verificar_servico()
    elif msg.lower() == '/dns':
        return obter_informacoes_dns()
    elif msg.lower() == '/map':
        return obter_mapa_de_rede()
    else:
        return "comando não reconhecido."


def enviar_resposta_telegram(texto,chat_id):
    try:
        url = f"{TELEGRAM_API_URL}/sendMessage"
        params= {"chat_id": chat_id, "text": texto}
        requests.get(url, params=params)
    except Exception as e:
        print(f"erro ao enviar resposta ao telegram:{str(e)}")
        
def processar_mensagem_telegram(texto,chat_id):
    response=processar_mensagem(texto)
    enviar_resposta_telegram(response,chat_id)

def verificar_novas_mensagens():
    offset=None

    while True:
        try:
            url =f"{TELEGRAM_API_URL}/getUpdates?offset={offset}"
            response = requests.get(url)
            data = response.json()

            if "result" in data and data["result"]:
                for update in data["result"]:
                    offset = update["update_id"] + 1
                    processar_mensagem_telegram(update["message"]["text"], update["message"]["chat"]["id"])

            time.sleep(1)  

        except Exception as e:
            print(f"erro ao verificar novas mensagens do telegram: {str(e)}")
            time.sleep(5) 
    

def conectar_e_executar():
    global tcp_socket, tentativas

    while True:
        try:
            tcp_socket.connect((HOST, PORT))
            print('Conexão estabelecida.')
            print()
            verificar_novas_mensagens()

        except (socket.error, ConnectionError):
            # Lidar com a desconexão
            print('Tentando conectar...')
            time.sleep(5)
            tentativas += 1
            print(f"Tentativa de conexão: {tentativas}")

            # Recriar o socket
            tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)







if __name__ == "__main__":
    conectar_e_executar()



