

#bot.py
import os
import subprocess
import requests


class TelegramBot:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id
        self.url_send_message =f"https://api.telegram.org/bot{token}/sendMessage"
        self.url_get_updates = f"https://api.telegram.org/bot{token}/getUpdates"

    def send_msg(self, texto):
        params = {"chat_id": self.chat_id, "text":texto}
        try:
            resposta = requests.get(self.url_send_message, params=params)
            resposta.raise_for_status()
            print(resposta.json())
        except requests.exceptions.RequestException as e:
            print(f"erro ao enviar mensagem:{e}")

    def processar_mensagem(self, msg):
        if msg.lower() == '/ola':
            return "Olá, meu amigo!"
        elif msg.lower() =='/info':
            return self.obter_informacoes_de_rede()
        elif msg.lower() == '/ping':
            return self.ping_google()
        elif msg.startswith('/active '):
            return self.verificar_resposta_ip(msg.split()[1])
        elif msg.startswith('/service '):
            return self.verificar_servico(msg.split()[1])
        elif msg.lower() == '/dns':
            return self.obter_informacoes_dns()
        elif msg.lower() == '/map':
            return self.obter_mapa_de_rede()
        else:
            return "comando não reconhecido!"

    def get_ultima_msg(self):
        try:
            resultado =requests.get(self.url_get_updates).json()['result']
            ultima_msg =resultado[-1]['message']['text']
            return ultima_msg
        except (KeyError, IndexError, requests.exceptions.RequestException) as e:
            print(f"erro ao obter a última mensagem:{e}")
            return None

    def obter_informacoes_de_rede(self):
        try:
            endereco_ip =os.popen('hostname -I').read().strip().split()[0]
            mascara_subrede ='255.255.255.0'
            gateway =os.popen("ip r | grep default | awk '{print $3}'").read().strip()
            return f"informações basicas sobre a rede:\nIP: {endereco_ip}\nMáscara: {mascara_subrede}\nGateway: {gateway}"
        except Exception as e:
            return f"erro ao obter informações de rede:{str(e)}"

    def ping_google(self):
        try:
            resultado =subprocess.run(['ping', '-c', '4', 'google.com'], capture_output=True, text=True).stdout
            return resultado
        except Exception as e:
            return f"erro ao executar o comando ping:{str(e)}"

    def verificar_resposta_ip(self, endereco_ip):
        try:
            resultado =subprocess.run(['ping', '-c', '4', endereco_ip], capture_output=True, text=True).stdout
            return resultado
        except Exception as e:
            return f"erro ao verificar a resposta do IP {endereco_ip}:{str(e)}"

    def verificar_servico(self, ip_and_port):
        try:
            ip, port =ip_and_port.split(':')
            resultado =subprocess.run(['nc', '-zv', ip, port], capture_output=True, text=True).stdout
            return resultado
        except Exception as e:
            return f"erro ao verificar o serviço em{ip_and_port}:{str(e)}"



    def obter_informacoes_dns(self):
        try:
            resultado =subprocess.run(['nslookup','google.com'],capture_output=True, text=True).stdout
            return resultado
        except Exception as e:
            return f"erro ao obter informações de DNS:{str(e)}"

    def obter_mapa_de_rede(self):
        try:
            resultado =subprocess.run(['arp', '-a'], capture_output=True, text=True).stdout
            return resultado
        except Exception as e:
            return f"erro ao obter o mapa de rede:{str(e)}"

token = "6958977609:AAE5X1-eA9spI7dXOfal1g7WWytgwWmvXeU"
#"6788315183:AAG6g041wJ2RmHX_1WHrqrzjcOyIhkCO5II"

chat_id = "6440731935"
#"6440731935"

bot = TelegramBot(token,chat_id)
msg = bot.get_ultima_msg()

if msg:
    resposta = bot.processar_mensagem(msg)
    bot.send_msg(resposta)
