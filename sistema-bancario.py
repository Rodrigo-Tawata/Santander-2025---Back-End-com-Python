import datetime


saldo = 0
limite = 500
extrato = []
numero_saques = 0
LIMITE_SAQUES = 3


# Data/Hora
def obter_data_hora():
    return datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")


# Depósito
def depositar(valor):
    global saldo
    if valor > 0:
        saldo += valor
        extrato.append({"tipo": "Depósito", "valor": valor,
                       "data": obter_data_hora()})
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")
    else:
        print("Operação falhou! O valor informado é inválido.")


# Saque
def sacar(valor):
    global saldo, numero_saques
    if valor <= 0:
        print("Operação falhou! O valor informado é inválido.")
    elif valor > saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif valor > limite:
        print("Operação falhou! O valor do saque excede o limite de R$ 500.")
    elif numero_saques >= LIMITE_SAQUES:
        print("Operação falhou! Número máximo de saques excedido.")
    else:
        saldo -= valor
        numero_saques += 1
        extrato.append({"tipo": "Saque", "valor": valor,
                       "data": obter_data_hora()})
        print(f"Saque de R$ {valor:.2f} realizado com sucesso.")


# Extrato
def exibir_extrato():
    print("\n================ EXTRATO ================")
    if not extrato:
        print("Não foram realizadas movimentações.")
    else:
        for operacao in extrato:
            print(
                f"{operacao['data']} - {operacao['tipo']}: R$ {operacao['valor']:.2f}")
    print(f"\nSaldo atual: R$ {saldo:.2f}")
    print("=========================================")


# Menu
def menu():
    return """
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
=> """


while True:
    opcao = input(menu()).lower()

    if opcao == "d":
        try:
            valor = float(input("Informe o valor do depósito: "))
            depositar(valor)
        except ValueError:
            print("Entrada inválida! Digite um número.")

    elif opcao == "s":
        try:
            valor = float(input("Informe o valor do saque: "))
            sacar(valor)
        except ValueError:
            print("Entrada inválida! Digite um número.")

    elif opcao == "e":
        exibir_extrato()

    elif opcao == "q":
        print("Obrigado por usar o sistema bancário. Até logo!")
        break

    else:
        print("Operação inválida! Selecione uma opção válida.")
