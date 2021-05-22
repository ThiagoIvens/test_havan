import sqlite3

# Classe para conexao e manipulação do banco de dados sqlite3
class Connect:

    # Inicia a conexao definindo o banco a ser conectado e o cursor para manipulação, alem de chamar a função responsavel pela criação das tabelas do banco
    def __init__(self) -> None:
        self.conn = sqlite3.connect('db.sqlite3')
        self.cursor = self.conn.cursor()
        self.create_table()

    # Função para criação das tabelas do banco de dados
    def create_table(self):
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS Cadastro (
                nome TEXT,
                mOrigem INTEGER,
                mDestino INTEGER,
                data DATE,
                valor INTEGER,
                valor_Convertido INTEGER,
                taxa INTEGER,
                valorDescTaxa INTEGER)''')

            self.cursor.execute('''CREATE TABLE IF NOT EXISTS Conversao (
                nome TEXT UNIQUE,
                valor INTEGER UNIQUE)''')
        except Exception as e:
            print('\n[ERROR] Falha ao criar tabela: \n', e)
        else:
            print('\nTabela criada com sucesso')

    # Função para inserir uma nova operação a tabela Cadastro
    def insert_operation(self, operacao):
        try:
            self.cursor.execute('''INSERT INTO Cadastro VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                (operacao.name, operacao.mOrigem, operacao.mDestino, operacao.data, operacao.valor, operacao.vConvertido, operacao.taxa, operacao.valorDescTaxa))
        except Exception as e:
            print('\n[ERROR] Falha ao inserir registro\n', e)
            self.conn.rollback()
        else:
            self.conn.commit()
            print('\nRegistro inserido com sucesso!')

    # Função para inserir uma nova conversão a tabela Conversao
    def insert_conversion(self, nome, valor):
        try:
            self.cursor.execute(
                '''INSERT INTO Conversao VALUES (?)''', valor)
        except Exception as e:
            print('\n[ERROR] Falha ao inserir registro\n', e)
        else:
            self.conn.commit()
            print('\nRegistro inserido com sucesso!')

    # Função para pegar uma operação por id na tabela Cadastro
    def get(self, id):
        return self.cursor.execute('''SELECT * FROM Cadastro WHERE rowid=?''', (id,)).fetchone()
    
    # Função para pegar o valor total de todas operações da tabela Cadastro
    def get_valor_total(self):
        return  self.cursor.execute('''SELECT SUM(valorDescTaxa) FROM Cadastro''', ).fetchone()
    
    # Função para pegar o valor total das taxas de todas operações da tabela Cadastro
    def get_valor_total_taxas(self):
        return  self.cursor.execute('''SELECT SUM(taxa) FROM Cadastro''', ).fetchone()

    # Função para pegar o valor total das conversões de todas operações da tabela Cadastro
    def get_valor_conversion(self, valor):
        return self.cursor.execute('''SELECT valor FROM Conversao WHERE nome=?''', (valor)).fetchone()

    # Função para pegar todas operações da tabela Cadastro
    def getAll(self, limit=10000):
        return  self.cursor.execute('''SELECT * FROM Cadastro LIMIT ?''', (limit,)).fetchall()

    # Função para pegar todas operações da tabela Cadastro ordenada pelo nome dos clientes
    def getAll_orderBy_client(self, limit=10000):
        return  self.cursor.execute('''SELECT * FROM Cadastro ORDER BY nome LIMIT ?''', (limit,)).fetchall()   
    
    # Função para pegar todas operações da tabela Cadastro ordenada pela data das operações
    def getAll_orderBy_date(self, limit=10000):
        return  self.cursor.execute('''SELECT * FROM Cadastro ORDER BY data LIMIT ?''', (limit,)).fetchall()
    
    # Função para pegar todas conversões cadastradas na tabela Conversao
    def getAll_conversion(self, limit=10000):
        return self.cursor.execute('''SELECT * FROM Conversao LIMIT ?''', (limit,)).fetchall()
    
    # Função para atualizar a operação cujo id fora informado da tabela Cadastro
    def update(self, id, operacao):
        try:
            self.cursor.execute(
                '''UPDATE Cadastro SET nome=?, mOrigem=?, mDestino=?, data=?, valor=?, valor_Convertido=?,
                taxa=? WHERE rowid=?''', (operacao.name, operacao.mOrigem, operacao.mDestino, operacao.data, operacao.valor, operacao.vConvertido, operacao.taxa, id))
        except Exception as e:
            print('\n[ERROR] Falha na alteração do registro\n', e)
        else:
            self.conn.commit()
            print('\nRegistro alterado com sucesso!')

    # Função para deletar a operação cujo id fora informado, da tabela Cadastro
    def delete(self, id):
        try:
            self.cursor.execute(
                '''DELETE FROM Cadastro WHERE rowid=?''', (id,))
        except Exception as e:
            print('\n[ERROR] Falha ao remover registro\n', e)
        else:
            self.conn.commit()
            print('\nRegistro removido com sucesso!')

    # Função para deletar a conversao cujo id fora informado, da tabela Conversao
    def delete_conversion(self, id):
        try:
            self.cursor.execute(
                '''DELETE FROM Conversao WHERE rowid=?''', (id,))
        except Exception as e:
            print('\n[ERROR] Falha ao remover registro\n', e)
        else:
            self.conn.commit()
            print('\nRegistro removido com sucesso!')