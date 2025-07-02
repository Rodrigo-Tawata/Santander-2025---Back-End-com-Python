# MÓDULOS E CLASSES JÁ DEFINIDAS
from abc import ABC, abstractmethod


class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)


class Conta:
    def __init__(self, numero: int, cliente, agencia: str = "000"):
        self._saldo = 0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    def sacar(self, valor: float):
        if valor > 0 and self._saldo >= valor:
            self._saldo -= valor
            return True
        return False

    def depositar(self, valor: float):
        if valor > 0:
            self._saldo += valor
            return True
        return False

    @classmethod
    def nova_conta(cls, cliente, numero: int):
        return cls(numero, cliente)


class ContaCorrente(Conta):
    def __init__(self, numero: int, cliente, limite: float, limite_saques: int, agencia: str = "000"):
        super().__init__(numero, cliente, agencia)
        self.limite = limite
        self.limite_saques = limite_saques
        self.numero_saques = 0

    def sacar(self, valor: float):
        if valor > self.limite:
            print("Valor excede o limite por saque.")
            return False
        if self.numero_saques >= self.limite_saques:
            print("Limite de saques atingido.")
            return False
        if super().sacar(valor):
            self.numero_saques += 1
            return True
        return False


class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta: Conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor: float):
        self.valor = valor

    def registrar(self, conta: Conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)
            print(f"Depósito de R$ {self.valor:.2f} realizado com sucesso.")
        else:
            print("Erro ao realizar o depósito.")


class Saque(Transacao):
    def __init__(self, valor: float):
        self.valor = valor

    def registrar(self, conta: Conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)
            print(f"Saque de R$ {self.valor:.2f} realizado com sucesso.")
        else:
            print("Erro ao realizar o saque.")


class Cliente:
    def __init__(self, endereco: str):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome: str, cpf: str, data_nascimento: str, endereco: str):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

# ====================== FUNÇÕES AUXILIARES ======================


def localizar_cliente(cpf, clientes):
    for cliente in clientes:
        if isinstance(cliente, PessoaFisica) and cliente.cpf == cpf:
            return cliente
    return None


def exibir_extrato(conta: Conta):
    print("\n================ EXTRATO ================")
    if not conta.historico.transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in conta.historico.transacoes:
            tipo = transacao.__class__.__name__
            valor = transacao.valor
            print(f"{tipo}: R$ {valor:.2f}")
    print(f"\nSaldo atual: R$ {conta.saldo:.2f}")
    print("==========================================\n")

# ====================== MENU PRINCIPAL ======================


def main():
    clientes = []
    contas = []
    AGENCIA = "000"

    menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[nu] Novo Usuário
[nc] Nova Conta
[lc] Listar Contas
[q] Sair

=> """

    while True:
        opcao = input(menu)

        if opcao == "nu":
            cpf = input("CPF (somente números): ")
            if localizar_cliente(cpf, clientes):
                print("Já existe cliente com esse CPF.")
                continue
            nome = input("Nome completo: ")
            nascimento = input("Data de nascimento (dd-mm-aaaa): ")
            endereco = input(
                "Endereço (logradouro, nro - bairro - cidade/UF): ")
            cliente = PessoaFisica(nome, cpf, nascimento, endereco)
            clientes.append(cliente)
            print("Usuário criado com sucesso.")

        elif opcao == "nc":
            cpf = input("CPF do titular: ")
            cliente = localizar_cliente(cpf, clientes)
            if not cliente:
                print("Cliente não encontrado.")
                continue
            numero_conta = len(contas) + 1
            conta = ContaCorrente(numero_conta, cliente,
                                  limite=500, limite_saques=3, agencia=AGENCIA)
            cliente.adicionar_conta(conta)
            contas.append(conta)
            print("Conta criada com sucesso.")

        elif opcao == "d":
            cpf = input("CPF do cliente: ")
            cliente = localizar_cliente(cpf, clientes)
            if not cliente or not cliente.contas:
                print("Cliente ou conta não encontrados.")
                continue
            valor = float(input("Valor do depósito: "))
            conta = cliente.contas[0]
            cliente.realizar_transacao(conta, Deposito(valor))

        elif opcao == "s":
            cpf = input("CPF do cliente: ")
            cliente = localizar_cliente(cpf, clientes)
            if not cliente or not cliente.contas:
                print("Cliente ou conta não encontrados.")
                continue
            valor = float(input("Valor do saque: "))
            conta = cliente.contas[0]
            cliente.realizar_transacao(conta, Saque(valor))

        elif opcao == "e":
            cpf = input("CPF do cliente: ")
            cliente = localizar_cliente(cpf, clientes)
            if not cliente or not cliente.contas:
                print("Cliente ou conta não encontrados.")
                continue
            conta = cliente.contas[0]
            exibir_extrato(conta)

        elif opcao == "lc":
            for conta in contas:
                print(f"""
Agência: {conta.agencia}
Número: {conta.numero}
Titular: {conta.cliente.nome}
""")
        elif opcao == "q":
            print("Encerrando o sistema.")
            break
        else:
            print("Opção inválida.")


# Executar sistema
if __name__ == "__main__":
    main()
