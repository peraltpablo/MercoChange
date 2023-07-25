import sqlite3
from cotação.conta import *
from historico.historico_de_conversao import *
 
conexao = sqlite3.connect("mercochange.db")
conexao.execute("PRAGMA foreign_keys = 1")
cursor = conexao.cursor()

while True:  
    h = input("Vamos fazer Login:\n1 - Acessar Conta \n2 - Cadastrar usuários\n3 - Administrador\n0 - Sair\nDigite opcão: ")
    match h:
        case "1":
            print("ACESSAR CONTA DO CLIENTE")
            usuario = input("Digite seu CPF: ")
            senha = input("Digite sua SENHA: ")
            cursor.execute(f'SELECT nome,cpf,senha FROM clientes WHERE cpf = ? AND senha=?' , [usuario, senha])
            dados = cursor.fetchone()
            if dados == None: # explicado em dados, essa Ã© a condiÃ§Ã£o de retorno.
                    print("--------------------------")
                    print("Usuario ou Senha Inválidos")
                    print("--------------------------")
            else:
                    print("------------------------------------")
                    print(f"Seja Bem Vindo a sua Conta: {dados[0]}")
                    print("------------------------------------")
                    while True:
                        p = input('Digite o que você deseja fazer:\n1 - Conta\n2 - Perfil\n0 - voltar\n ')
                        while p != "1" and p != "2" and p != "3" and p != "0":
                            p = input('Digite o que você deseja fazer:\n1 - Conta\n2 - Perfil\n0 - voltar\n ')
                        match p:
                            case "1":
                                while True:
                                    menu = input("\n***MERCOCHANGE***\n1 - Depositar Dinheiro\n2 - Ver Cotação\n3 - Comprar / Vender Moeda\n4 - Saldo\n5 - Sacar Dinheiro\n6 - Ver Histórico\n0 - Sair\nDigite opcão: ")
                                    while menu != "1" and menu != "2" and menu != "3" and menu != "4" and menu != "5" and menu != "6" and menu != "0":
                                        menu = input("\n***Opção Invãlida!! - ***MERCOCHANGE***\n1 - Depositar Dinheiro\n2 - Ver Cotação\n3 - Comprar / Vender Moeda\n4 - Saldo\n5 - Sacar Dinheiro\n6 - Ver Histórico\n0 - Sair\nDigite opcão: ")
                                    match menu:
                                        case "1":
                                            deposito = input("Valor á Depositar: ")
                                            try:
                                                float(deposito)
                                            except:
                                                print("Valor Inválido")

                                            else:
                                                deposito = float(deposito)
                                                if deposito > 0:
                                                    c1.depositar(usuario,"BRL",deposito)
                                                else:
                                                    print("O depósito deve ser maior que 0")
                                        case "2":
                                            import time
                                            date=time.strftime('%d-%m-%y %H:%M:%S', time.localtime())
                                            moedas = ["ARS","PYG","UYU","BTC"]
                                            print(f"\n**COTAÇÕES - BRL {date}")
                                            for moeda in moedas:
                                                c1.cotacao(moeda)
                                            print("Cotação Bolívar Venezuelano indisponível devido a suspensão da Venezuela do Mercosul por tempo indeterminado.")
                                        case "3":
                                            compra = input("\n**VOCÊ COMPRA:\n1 - Real Brasileiro\n2 - Peso Argentino\n3 - Guarani Paraguaio\n4 - Peso Uruguaio\n5 - Bolívar Venezuelano (Indisponivel)\n6 - Bitcoin\n0 - Sair\nDigite opcão: ")
                                            while compra != "1" and compra != "2" and compra != "3" and compra != "4" and compra != "6" and compra != "0":
                                                compra = input("\n**!!!!Erro opção indisponivel!!!!\nVOCÊ COMPRA:\n1 - Real Brasileiro\n2 - Peso Argentino\n3 - Guarani Paraguaio\n4 - Peso Uruguaio\n5 - Bolívar Venezuelano (Indisponivel)\n6 - Bitcoin\n0 - Sair\nDigite opcão: ")
                                            match compra:
                                                case "1":
                                                    comprar = "BRL"
                                                case "2":
                                                    comprar = "ARS"
                                                case "3":
                                                    comprar = "PYG"
                                                case "4":
                                                    comprar = "UYU"
                                                case "6":
                                                    comprar = "BTC"
                                                case "0":
                                                    break
                                            quantidade = input("Quantidade á Comprar (0 para sair): ")
                                            while quantidade == "" or quantidade.isnumeric() == False:
                                                quantidade = input("\n***Valor INVÁLIDO. Digite Novamente a Quantidade a Comprar: ")
                                            if quantidade == "0":
                                                break
                                            quantidade = float(quantidade)
                                            venda = input("\n**VOCÊ PAGA:\n1 - Real Brasileiro\n2 - Peso Argentino\n3 - Guarani Paraguaio\n4 - Peso Uruguaio\n5 - Bolívar Venezuelano (Indisponivel)\n6 - Bitcoin\n0 - Sair\nDigite opcão: ")
                                            while venda != "1" and venda != "2" and venda != "3" and venda != "4" and venda != "6" and venda != "0":
                                                venda = input("\n**!!!!Erro Opção Indisponivel!!!!\nVOCÊ PAGA:\n1 - Real Brasileiro\n2 - Peso Argentino\n3 - Guarani Paraguaio\n4 - Peso Uruguaio\n5 - Bolívar Venezuelano (Indisponivel)\n6 - Bitcoin\n0 - Sair\nDigite opcão: ")
                                            match venda:
                                                case "1":
                                                    vender = "BRL"
                                                case "2":
                                                    vender = "ARS"
                                                case "3":
                                                    vender = "PYG"
                                                case "4":
                                                    vender = "UYU"
                                                case "6":
                                                    vender = "BTC"
                                                case "0":
                                                    break
                                            if compra == venda:
                                                print("**As moedas da transação devem ser diferentes!")
                                            else:
                                                c1.comprar(comprar,quantidade,vender,usuario)
                                        case "4":
                                            c1.mostrar_saldo(usuario)
                                        case "5":
                                            saque = input("Valor à Sacar: ")
                                            while saque == "" or saque == "0" or saque.isnumeric() == False:
                                                saque = input("\n***Valor Inválido. Digite Novamente o Valor à Sacar: ")
                                            saque = float(saque)
                                            c1.sacar(usuario,"BRL",saque)
                                        case "6":
                                            historico.mostrar_historico(usuario)
                                        case "0":
                                            break
                            case "2":
                                while True:
                                    r = input('Digite o que você deseja fazer:\n1 - Alterar Senha\n2 - Deletar Conta\n3 - Mostrar Conta\n0 - Voltar\nDigite opcão: ')
                                    while r != "1" and r != "2" and r != "3" and r != "0":
                                        r = input('**Opção Inválida. Digite o que você deseja fazer:\n1 - Alterar Senha\n2 - Deletar Conta\n3 - Mostrar Conta\n0 - Voltar\nDigite opcão: ')
                                    match r:
                                            case "1":
                                                c1.alterar_senha(usuario)
                                            case "2":
                                                c1.excluir_conta(usuario)
                                            case "3":
                                                c1.mostrar_conta(usuario)
                                            case "0":
                                                break
                            case "0":
                                break
        case "2":
            try:
                n = str(input('Digite o seu NOME: \n')).capitalize()
                while len(n) < 3:
                    n = str(input('Digite um NOME válido de no mínimo 3 carateres: \n')).capitalize()
                c = input('Digite seu CPF : \n')
                while Conta.validate (str(c)) == False:
                    c = input('**CPF Inválido!!. Digite seu CPF : \n')
                p = str(input('Digite o seu PIX: \n'))
                while len(p) < 11:
                    p = str(input('Digite um PIX válido de no mínimo 11 carateres: \n'))
                e = str(input('Digite a seu EMAIL: \n'))
                while "@" not in e or ".com" not in e:
                    e = str(input('Digite um EMAIL válido: \n'))
                s = str(input('Digite a sua SENHA: \n'))
                while len(s) < 8:
                    s = str(input('Digite uma SENHA no mínimo de 8 carateres: \n'))
                c1.criar_conta(n,c,p,e,s)
                print("Usuário Criado com Sucesso!\nPara acessar utilize CPF e SENHA.")
            except sqlite3.IntegrityError:
                print("Este CPF ou Email já possui Usuário Cadastrado")
        case "3":
            secreto = input('Digite o Código secreto para ver a senha e o login das contas: (Código deve ter 4 números)\n')
            if secreto == "1234":
                while True:
                    r1= input("Digite o Número da Opção que deseja:\n1 - Ver todas as Contas\n2 - Excluir Contas\n3 - Ver Históricos\n0 - Sair\nDigite opcão: ")
                    while r1 != "1" and r1 != "2" and r1 != "3" and r1 != "0":
                        r1= input("Digite o Número da Opção que deseja:\n1 - Ver todas as Contas\n2 - Excluir Contas\n3 - Ver Históricos\n0 - Sair\nDigite opcão: ")
                    match r1: 
                            case "1":
                                c1.ver_conta()
                            case "2":
                                c1.excluir_conta_adm()
                            case "3":
                                historico.mostrar_historico_adm()
                            case "0":
                                break
            else:
                print("**Senha Inválida!")
        case "0":
            break
        case _:
            print("\n**Opção Inválida!!!\n")
cursor.close()
conexao.close()