from datetime import date
import textwrap


class PessoaFisica:
    def __init__(self, nome, cpf, data_nascimento):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento


class Cliente(PessoaFisica):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(nome, cpf, data_nascimento)
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)


class Conta:
    def __init__(self, cliente, numero):
        self.saldo = 0
        self.numero = numero
        self.agencia = "0001"
        self.cliente = cliente
        self.historico = Historico()

    def saldo_atual(self):
        return self.saldo

    def sacar(self, valor):
        if valor <= 0 or valor > self.saldo:
            print("\n@@@ Saque inválido. Verifique o valor. @@@")
            return False

        self.saldo -= valor
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("\n@@@ Depósito inválido. Verifique o valor. @@@")
            return False

        self.saldo += valor
        return True


class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite=500, limite_saques=3):
        super().__init__(cliente, numero)
        self.limite = limite
        self.limite_saques = limite_saques
        self.numero_saques = 0

    def sacar(self, valor):
        if self.numero_saques >= self.limite_saques:
            print("\n@@@ Limite de saques atingido. @@@")
            return False
        if valor > self.limite:
            print("\n@@@ Valor excede o limite de saque. @@@")
            return False
        if super().sacar(valor):
            self.numero_saques += 1
            return True
        return False


class Transacao:
    def registrar(self, conta):
        raise NotImplementedError


class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


# ================= FUNÇÕES DO MENU =================

def menu():
    opcoes = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(opcoes))


def exibir_extrato(conta):
    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes
    if not transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in transacoes:
            tipo = transacao.__class__.__name__
            print(f"{tipo}:\tR$ {transacao.valor:.2f}")
    print(f"\nSaldo:\t\tR$ {conta.saldo:.2f}")
    print("==========================================")


def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ").strip()

    if any(usuario.cpf == cpf for usuario in usuarios):
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço: ")

    novo_usuario = Cliente(nome, cpf, data_nascimento, endereco)
    usuarios.append(novo_usuario)

    print("=== Usuário criado com sucesso! ===")


def filtrar_usuario(cpf, usuarios):
    for usuario in usuarios:
        if usuario.cpf == cpf:
            return usuario
    return None


def criar_conta(numero, usuarios):
    cpf = input("Informe o CPF do usuário: ").strip()
    cliente = filtrar_usuario(cpf, usuarios)

    if cliente:
        conta = ContaCorrente(cliente, numero)
        cliente.adicionar_conta(conta)
        print("\n=== Conta criada com sucesso! ===")
        return conta

    print("\n@@@ Usuário não encontrado! @@@")
    return None


def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(f"Agência:\t{conta.agencia}")
        print(f"C/C:\t\t{conta.numero}")
        print(f"Titular:\t{conta.cliente.nome}")


# ================= EXECUÇÃO =================

def main():
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            cpf = input("Informe o CPF do titular: ")
            cliente = filtrar_usuario(cpf, usuarios)

            if cliente and cliente.contas:
                conta = cliente.contas[0]
                valor = float(input("Informe o valor do depósito: "))
                cliente.realizar_transacao(conta, Deposito(valor))
            else:
                print("\n@@@ Cliente ou conta não encontrada. @@@")

        elif opcao == "s":
            cpf = input("Informe o CPF do titular: ")
            cliente = filtrar_usuario(cpf, usuarios)

            if cliente and cliente.contas:
                conta = cliente.contas[0]
                valor = float(input("Informe o valor do saque: "))
                cliente.realizar_transacao(conta, Saque(valor))
            else:
                print("\n@@@ Cliente ou conta não encontrada. @@@")

        elif opcao == "e":
            cpf = input("Informe o CPF do titular: ")
            cliente = filtrar_usuario(cpf, usuarios)

            if cliente and cliente.contas:
                conta = cliente.contas[0]
                exibir_extrato(conta)
            else:
                print("\n@@@ Cliente ou conta não encontrada. @@@")

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(numero_conta, usuarios)
            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            print("Saindo do sistema. Até logo!")
            break

        else:
            print("\n@@@ Opção inválida! @@@")

main()
