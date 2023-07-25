import requests
import sqlite3
from historico.historico_de_conversao import *

conexao = sqlite3.connect("mercochange.db")
conexao.execute("PRAGMA foreign_keys = 1")
cursor = conexao.cursor()

class Conta:
    def criar_conta(self,nome ,cpf ,pix,email ,senha ):        
        self.nome = nome
        self.cpf = cpf
        self.pix = pix
        self.email = email
        self.senha = senha
        comand.execute('CREATE TABLE IF NOT EXISTS clientes('
        'id INTEGER PRIMARY KEY AUTOINCREMENT,'
        'nome TEXT NOT NULL,'
        'cpf INTEGER NOT NULL UNIQUE,'
        'pix TEXT NOT NULL UNIQUE,'
        'email TEXT NOT NULL UNIQUE,'
        'senha TEXT'')')
        cursor.execute('INSERT INTO clientes(nome,cpf,pix,email,senha) VALUES(?,?,?,?,?)',(nome,cpf,pix,email,senha))
        comand.execute('CREATE TABLE IF NOT EXISTS carteira('
        'CPF INTEGER PRIMARY KEY,'
        'BRL REAL,'
        'ARS REAL,'
        'PYG REAL,'
        'UYU REAL,'
        'BOL REAL,'
        'BTC REAL,'
        'FOREIGN KEY(CPF) REFERENCES clientes(cpf) ON DELETE CASCADE ON UPDATE CASCADE'
        ')')
        cursor.execute('INSERT INTO carteira(CPF,BRL,ARS,PYG,UYU,BOL,BTC) VALUES(?,?,?,?,?,?,?)',(cpf,0,0,0,0,0,0))
        conexao.commit()
    def excluir_conta(self,cpf):
        cursor.execute(f'SELECT * FROM clientes WHERE cpf = "{cpf}"')
        for linha in cursor.fetchall():
            a,b,c,d,e,f = linha
            print(f"Id: {a}. Nome: {b}. CPF: {c}. PIX: {d}. Email: {e}. Senha: {f}.")
        confirmaçao = input("Está seguro que Deseja Exluir a Conta? (S/N): ").upper()
        while confirmaçao != "S" and confirmaçao !="N":
            confirmaçao = input("Digite S ou N. Está seguro que Deseja Exluir a Conta? (S/N): ").upper()
        if confirmaçao == "S":
            cursor.execute('DELETE FROM clientes WHERE cpf = ?',(cpf,) )
            conexao.commit()
            print("Conta Excluida com Sucesso!")
            exit()
    def alterar_senha(self,cpf):
        cursor.execute(f'SELECT cpf,senha FROM clientes WHERE cpf = "{cpf}"')
        for linha in cursor.fetchall():
            a,b = linha
            print(f"CPF: {a}. Senha atual: {b}")
        r = str(input("Digite a Nova Senha que deseja inserir :\n"))
        while len(r) < 8:
            r = str(input('Digite uma SENHA no mínimo de 8 carateres: \n'))
        cursor.execute(f'UPDATE clientes SET  senha = ? WHERE cpf = "{cpf}"',(r,))    
        conexao.commit()
        cursor.execute(f'SELECT cpf,senha FROM clientes WHERE cpf = "{cpf}"')
        for linha in cursor.fetchall():
            a,b = linha
            print(f"\nAlteração com sucesso!\nCPF: {a}. Senha atual: {b}\n")
    def mostrar_conta(self,cpf):
        cursor.execute(f'SELECT * FROM clientes WHERE cpf = "{cpf}"')
        for linha in cursor.fetchall():
            a,b,c,d,e,f = linha
            print(f"Id: {a}. Nome: {b}. CPF: {c}. PIX: {d}. Email: {e}. Senha: {f}.")
    @staticmethod
    def validate(cpf: str):

        # Obtém apenas os números do CPF, ignorando pontuações
        numbers = [int(digit) for digit in cpf if digit.isdigit()]

        # Verifica se o CPF possui 11 números ou se todos são iguais:
        if len(numbers) != 11 or len(set(numbers)) == 1:
            return False

        # Validação do primeiro dígito verificador:
        sum_of_products = sum(a*b for a, b in zip(numbers[0:9], range(10, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[9] != expected_digit:
            return False

        # Validação do segundo dígito verificador:
        sum_of_products = sum(a*b for a, b in zip(numbers[0:10], range(11, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[10] != expected_digit:
            return False
        return True
    def excluir_conta_adm(self):
        try:
            cursor.execute(f'SELECT * FROM clientes \n')
            if cursor.fetchone() == None:
                print("\nAinda não tem Perfis")
            else:
                print("Contas")
                lista_ids = []
                cursor.execute(f'SELECT * FROM clientes \n')
                for linha in cursor.fetchall():
                    a,b,c,d,e,f = linha
                    print(f"Id: {a}. Nome: {b}. CPF: {c}. PIX: {d}. Email: {e}. Senha: {f}.")
                    lista_ids.append(a)
                r1 = input('Digite o ID da Conta que você deseja deletar:\n')
                if r1.isnumeric() == False:
                    print("**O ID digitado náo é numérico. Tente novamente\n")
                else:
                    if int(r1) in lista_ids:
                        confirmaçao = input("Está segur@ que Deseja Exluir a Conta? (S/N): ").upper()
                        while confirmaçao != "S" and confirmaçao !="N":
                            confirmaçao = input("Digite S ou N. Está seguro que Deseja Exluir a Conta? (S/N): ").upper()
                        if confirmaçao == "S":
                            cursor.execute('DELETE FROM clientes WHERE id = ?',(r1,) )
                            conexao.commit()
                            print("Conta Excluida com Sucesso!\n")
                            c1.ver_conta()
                    else:
                        print("**O ID digitado não pertence a nenhuma Conta Ativa!")
        except sqlite3.OperationalError:
            print("Ainda náo tem Contas Cadastradas\n")
    def ver_conta(self):
        try:
            cursor.execute(f'SELECT * FROM clientes \n')
            if cursor.fetchone() == None:
                print("\nAinda não tem Perfis")
            else:
                print("Na sua Conta tem os Perfis Abaixo: \n")
                cursor.execute(f'SELECT * FROM clientes \n')
                for linha in cursor.fetchall():
                    a,b,c,d,e,f = linha
                    print(f"Id: {a}. Nome: {b}. CPF: {c}. PIX: {d}. Email: {e}. Senha: {f}.")
        except sqlite3.OperationalError:
            print("Ainda náo tem Contas Cadastradas\n")
    def cotacao(self,moeda):
        info = requests.get(f'https://economia.awesomeapi.com.br/last/{moeda}').json()
        compra = info[f"{moeda}BRL"]["high"]
        venda = info[f"{moeda}BRL"]["low"]
        print(f"{moeda}-BRL - Compra: R$:{compra} --> Venda: R$:{venda}")
    def mostrar_saldo(self,cpf):
        cursor.execute(f'SELECT * FROM carteira WHERE cpf = "{cpf}"')
        for linha in cursor.fetchall():
            a,b,c,d,e,f,g = linha
            print(f"\nCPF: {a}\nReal: {b:.2f}\nPeso Argentino: {c:.2f}\nGuarani Paraguaio: {d:.2f}\nPesos Uruguaio: {e:.2f}\nBolivar Venezuelano: {f:.2f}\nBitcoin: {g:.2f} ")
    def depositar(self,cpf,moeda,deposito):
        cursor.execute(f'SELECT {moeda} FROM carteira WHERE cpf = "{cpf}"')
        saldo = 0
        for linha in cursor.fetchall():
            saldo = linha[0]
        cursor.execute(f'UPDATE carteira SET {moeda} = ? WHERE cpf = "{cpf}"',(saldo+deposito,))    
        conexao.commit()
        print(f"Você depositou R$:{deposito} em sua carteira.")
        historico.criar_historico(cpf,deposito,moeda,"Depósito",moeda) #todo inserir quantidade, moeda de entrada e moeda de saida
        historico.adicionar_historico()#Adiciona Historico
    def sacar(self,cpf,moeda,saque):
        cursor.execute(f'SELECT {moeda} FROM carteira WHERE cpf = "{cpf}"')
        if cursor.fetchone() == None:
            print("\nNão tem Saldo Disponível em Reais")
        else:
            cursor.execute(f'SELECT {moeda} FROM carteira WHERE cpf = "{cpf}"')
            for linha in cursor.fetchall():
                saldo = linha[0]
            if saque > saldo:
                print("##O valor que está tentando sacar é Maior à o seu Saldo!")
            else:
                cursor.execute(f'UPDATE carteira SET {moeda} = ? WHERE cpf = "{cpf}"',(saldo-saque,))    
                conexao.commit()
                c1.mostrar_saldo(cpf)
                print(f"Você sacou R$:{saque} da sua carteira pelo PIX.")
                historico.criar_historico(cpf,-saque,moeda,"Saque",moeda) #todo inserir quantidade, moeda de entrada e moeda de saida
                historico.adicionar_historico()#Adiciona Historico
    def comprar(self,comprar,quantidade,vender,cpf): #Parametros: moeda a comprar, quantidade, com qué moeda compra, cpf
        if comprar == "BRL": #REAL é a moeda meio. O que vocé compra se converte para Reais, por isso se compra RS, a cotação é 1
            cotacaoCompra = 1
        else:
            infoCompra = requests.get(f'https://economia.awesomeapi.com.br/last/{comprar}').json()
            if comprar == "BTC": #As cotações vem com . como separador decimal. O BTC ussa o . para separar milhares, aqui elimino esse .
                cotacaoCompra = float(infoCompra[f"{comprar}BRL"]["high"].replace(".",""))
            else: #Se não é BTC, só converto a cotação em dado float
                cotacaoCompra = float(infoCompra[f"{comprar}BRL"]["high"])
        if vender == "BRL": #REAL é a moeda meio. Se vocé vende Reais, a quantidade já é real, oseja, a cotação é 1
            cotacaoVenda = 1
        else:
            if vender == "BTC": #Mesma coisa de tirar o ponto se é BTC e depois calcula cotação
                infoCompra = requests.get(f'https://economia.awesomeapi.com.br/last/{vender}').json()
                cotacaoVenda = 1/float(infoCompra[f"{vender}BRL"]["low"].replace(".",""))
            else: #Se náo é BTC, só converte a float
                infoVenda = requests.get(f'https://economia.awesomeapi.com.br/last/BRL-{vender}').json()
                cotacaoVenda = float(infoVenda[f"BRL{vender}"]["low"])
        cotacaoOperacao = cotacaoCompra*cotacaoVenda #Multiplica cotações para obter Cotação Final
        cursor.execute(f'SELECT {vender} FROM carteira WHERE cpf = "{cpf}"')
        for linha in cursor.fetchall():
            saldoVender = linha[0] #Mostra o saldo da moeda com que você paga
        valorTotal = quantidade * cotacaoOperacao #Multiplica quantidade a comprar por Cotação Final
        print(f"Resumo da Operacão: Compra de {comprar} {quantidade}. Cotação: {vender} {cotacaoOperacao}. Total Operação: {vender} {valorTotal:.2f}.")
        confirmaçao = input("Confirma Operaçáo? (S/N): ").upper()
        while confirmaçao != "S" and confirmaçao !="N":
            confirmaçao = input("Digite S ou N. Está seguro que Deseja Exluir a Conta? (S/N): ").upper()
        if confirmaçao == "S":
            if valorTotal > saldoVender: #Se o saldo da moeda que paga é menor al Total da Operação
                print(f"Saldo INSUFICIENTE para fazer esta Operacão!. Saldo: {vender} {saldoVender:.2f}")
            else: #Se o saldo permite a compra
                cursor.execute(f'SELECT {comprar} FROM carteira WHERE cpf = "{cpf}"')
                for linha in cursor.fetchall():
                    saldoComprar = linha[0] #Saldo da moeda que compra
                cursor.execute(f'UPDATE carteira SET {comprar} = ? WHERE cpf = "{cpf}"',(saldoComprar+quantidade,))#Atualiza saldo moeda comprada
                conexao.commit()
                cursor.execute(f'UPDATE carteira SET {vender} = ? WHERE cpf = "{cpf}"',(saldoVender-valorTotal,))#Atualiza saldo moeda pagada  
                conexao.commit()
                c1.mostrar_saldo(cpf)
                historico.criar_historico(cpf,quantidade,comprar,vender,valorTotal) #todo inserir quantidade, moeda de entrada e moeda de saida
                historico.adicionar_historico()#Adiciona Historico
c1=Conta()