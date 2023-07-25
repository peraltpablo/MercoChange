import sqlite3 #importar função banco de dados 
import datetime #importar função para mostrar data e hora

conexao=sqlite3.connect("mercochange.db")
conexao.execute("PRAGMA foreign_keys = 1")
comand=conexao.cursor()
class Historico:# class cotação que solicita 3 argumentos obrigatoríos para fazer conversão.
    def criar_historico(self,cpf,quantidade,moeda_comprada,moeda_vendida,valor_venda) -> None:
        self.cpf = cpf
        self.quantidade = quantidade
        self.moeda_comprada = moeda_comprada
        self.moeda_vendida = moeda_vendida
        self.valor_venda = valor_venda

    def adicionar_historico(self): #função mostrar hora e data.
        agora = datetime.datetime.now() #variavel para mostrar data e horario da transação
        hora= (agora.strftime('%H:%M:%S')) # variavel para mostrar hora formatada no padrão BRASIL
        data= (agora.strftime('%D')) # variavel para mostrar hora data em numeros no padrão BRASIL
        conexao=sqlite3.connect("mercochange.db")
        conexao.execute("PRAGMA foreign_keys = 1")
        comand=conexao.cursor()
        comand.execute('CREATE TABLE IF NOT EXISTS historico('
        'id INTEGER PRIMARY KEY AUTOINCREMENT,'
        'cpf TEXT,'
        'hora TEXT,'
        'data TEXT,'
        'quantidade REAL,'
        'comprada TEXT,'
        'valor_venda REAL,'
        'vendida TEXT,'
        'FOREIGN KEY(cpf) REFERENCES clientes(cpf) ON DELETE CASCADE ON UPDATE CASCADE'
        ')')
        comand.execute('INSERT INTO historico(cpf,hora,data,quantidade,comprada,vendida,valor_venda) VALUES(?,?,?,?,?,?,?)',(self.cpf,hora,data,self.quantidade,self.moeda_comprada,self.moeda_vendida,self.valor_venda))
        conexao.commit()
        
    def deletar_banco(self):
        deletar= (input("Insira o ID que deseja DELETAR: "))
        comand.execute(f'DELETE FROM historico WHERE id = "{deletar}"')
        conexao.commit()
        comand.execute('SELECT * FROM historico')
        print (f"{deletar} foi REMOVIDO do banco de dados")
    
    def mostrar_historico(self,cpf):
        comand.execute(f'SELECT * FROM historico WHERE cpf = "{cpf}"')
        if comand.fetchone() == None:
            print("\nAinda não tem Histórico")
        else:
            comand.execute(f'SELECT * FROM historico WHERE cpf = "{cpf}"')
            for linha in comand.fetchall():
                a,b,c,d,e,f,g,h = linha
                print(f"Id: {a}. CPF: {b}. Hora: {c}. Data: {d}. Quantidade Comprada: {f} {e}. Pagou com: {h} {g}.")

    def mostrar_historico_adm(self):
        try:
            comand.execute(f'SELECT * FROM historico')
            if comand.fetchone() == None:
                print("\nAinda não tem Histórico")
            else:
                comand.execute(f'SELECT * FROM historico')
                for linha in comand.fetchall():
                    a,b,c,d,e,f,g,h = linha
                    print(f"Id: {a}. CPF: {b}. Hora: {c}. Data: {d}. Quantidade Comprada: {f} {e}. Pagou com: {h} {g}.")
        except sqlite3.OperationalError:
            print("Ainda náo tem Históricos\n")

historico = Historico()