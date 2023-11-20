# ProgRedes-2023.2
Descrição do Projeto
Este projeto consiste em uma aplicação cliente/servidor que permite monitorar e interagir com agentes remotos. O cliente (agente) é executado nos computadores dos usuários, coletando informações sobre o sistema e respondendo a comandos do servidor. O servidor gerencia múltiplas conexões de clientes simultaneamente e fornece comandos remotos por meio de um bot no Telegram.

Tecnologias Utilizadas
Socket: A comunicação entre o cliente e o servidor é realizada por meio de sockets TCP. Essa escolha proporciona uma comunicação confiável e bidirecional, permitindo uma troca eficiente de dados entre as partes.
Estrutura do Projeto
Cliente:

Ao ser executado, o cliente informa ao servidor que está online, fornecendo o nome do HOST, IP e usuário logado no sistema.
Execução em segundo plano: O cliente é projetado para ser executado em segundo plano, liberando o terminal para o usuário após a inicialização.
Verificação periódica do status do servidor: Caso o servidor esteja offline, o cliente verifica periodicamente se o servidor voltou online.
Impedimento de múltiplas instâncias: Garante que apenas uma instância do cliente seja carregada na memória.
Remoção do cliente da memória: Implementa uma forma para o cliente se remover da memória.
Servidor:

Suporte a múltiplas conexões: O servidor permite a conexão simultânea de vários clientes (agentes).
Gerenciamento de conexões: Detecta quando um cliente fica offline e gerencia as conexões ativas.
Execução em segundo plano: O servidor é projetado para ser executado em segundo plano, liberando o terminal para o usuário após a inicialização.
Impedimento de múltiplas instâncias: Garante que apenas uma instância do servidor seja carregada na memória.
Remoção do servidor da memória: Implementa uma forma para o servidor se remover da memória.
Comandos remotos via Telegram:
Informações do hardware.
Lista de programas instalados (compatível com Windows e Linux).
Histórico de navegação em navegadores específicos (Chrome, Firefox, Microsoft Edge, Opera e Safari).
Informações detalhadas do usuário logado (compatível com Windows e Linux).
Lista de agentes online com detalhes (IP, nome do HOST, usuário logado e tempo online).

REQUESITOS


