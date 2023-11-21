# ProgRedes-2023.2
1-INTRODUÇÃO

Este é um projeto de uma aplicação cliente/servidor para monitoramento remoto. A aplicação permite que um servidor solicite informações sobre o hardware, programas instalados, histórico de navegação e detalhes do usuário de agentes clientes. A comunicação entre o cliente e o servidor ocorre por meio de sockets TCP.

2-CONFIGURAÇÃO DO AMBIENTE 

requisitos:
<br>
Python 3.x
<br>
Instalação Clone este repositório: https://github.com/MeloAnaa/ProgRedes-2023.2/tree/main/PROJETO
<br>
Navegue até o diretório do projeto: cd PROJETO

USO DA APLICAÇÃO

Cliente (Agente)

Inicialização:
<pre>
  python cliente.py
</pre>

Funcionalidades:
<br>
-Informa ao servidor que está online com o nome do HOST, IP e usuário logado.
<br>
-Executa em segundo plano.
<br>
-Testa periodicamente se o servidor está online.
<br>
-Evita múltiplas instâncias na memória.
<br>
-Permite a remoção da memória.
<br>
-Responde a requisições do servidor.
<br>

3-SERVIDOR

Inicialização:
<pre>
  python servidor.py
</pre>

Funcionalidades:
<br>
-Permite conexão simultânea de vários clientes.
<br>
-gerencia conexões ativas e detecta clientes offline.
<br>
-Executa em segundo plano.
<br>
-Evita múltiplas instâncias na memória.
<br>
-Permite a remoção da memória.
<br>
-Comandos disponíveis via bot no Telegram:
<br>
/hardware: Obtém informações do hardware.
<br>
/programas: Obtém a lista de programas instalados.
<br>
/historico: Obtém o histórico de navegação.
<br>
/usuario: Obtém detalhes do usuário logado.
<br>
/agentes_online: Lista os agentes online com suas informações.



4-ESCOLHA O PROTOCOLO

O protocolo escolhido para a comunicação entre o cliente e o servidor é o TCP. Isso se deve à necessidade de uma comunicação confiável, garantindo que os dados sejam entregues sem perda, na ordem correta e sem duplicatas. Além disso, o TCP oferece controle de congestionamento, o que é crucial para garantir um desempenho eficiente na transmissão de dados em redes.


AS PRINCIPAIS FUNCIONALIDADES DA APLICACAO CLIENTE SÃO

-Informar ao servidor que está on-line.
<br>
-Responder a requisições do servidor.
<br>
-Verificar se o servidor está on-line.
<br>
-As principais funcionalidades da aplicação servidora são:
<br>
-Gerenciar as conexões com os clientes.
<br>
-Responder às requisições dos clientes.
<br>
-Detectar quando um cliente fica off-line.
<br>
-A aplicação cliente e servidor serão executadas em segundo plano e não permitirão que uma segunda instância delas seja carregada na memória.
<br>
-Além disso, as aplicações terão uma forma para se remover da memória.


