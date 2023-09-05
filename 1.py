import random
try:
    
    quantidade_valores = int(input("Digite a quantidade de valores: "))
    numeros_aleatorios = []

    for i in range(quantidade_valores):
        numero_aleatorio = random.randint(1, 1000000)  # Gere um número aleatório entre 1 e 100 (ajuste o intervalo conforme necessário)
        numeros_aleatorios.append(numero_aleatorio)

    print("Números aleatórios:", numeros_aleatorios)

    with open('lista_nao_ordenada.txt', 'w') as arquivo:
        for numero in numeros_aleatorios:
            arquivo.write(str(numero) + '\n')

    print("Lista salva em 'lista_nao_ordenada.txt'.")
except ValueError:
    print("Erro: Digite um número válido para a quantidade de valores.")
except IOError:
    print("Erro ao abrir/salvar o arquivo 'lista_nao_ordenada.txt'. Verifique as permissões ou o caminho do arquivo.")
except Exception as e:
    print(f"Erro inesperado: {str(e)}")
