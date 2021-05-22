import os
from datetime import date
from Operation import Operation
from Conn import Connect
from decimal import Decimal

# Intancia do banco de dados
conn = Connect()

# Menu de criação de uma nova operação, onde é preenchido os dados necessários e retornado um objeto contendo eles
def new_operation():
    name = input("Nome do Cliente: ")
    mOrigem = float(input("Valor da moeda de origem: "))
    mDestino = float(input("Valor da moeda de destino: "))
    data = date.today().strftime('%d, %m %Y')
    valor = float(input("Valor à ser convertido: "))
    vConvertido = (valor * mOrigem) * mDestino
    choose = input("Usar valor de conversao cadastrado? [s/n]")
    if (choose == 's'):
        conversion = conn.get_valor_conversion(input("Digite o nome de atalho da conversão: "))
    else:
        conversion = int(input("Valor da conversao (em porcentagem): "))
    if(conversion != 0):
        taxa = vConvertido * (conversion/100)
    else:
        taxa = 0
    valorDescTaxa = vConvertido - taxa

    operation_object = Operation(name, format(mOrigem, '.2f'), format(mDestino, '.2f'), data, format(valor, '.2f'), format(vConvertido, '.2f'), format(taxa, '.2f'), format(valorDescTaxa, '.2f'))
    return operation_object

# Menu de criação de uma nova conversão
def new_conversion():
    nome = input("\nNome de atalho para conversao: ")
    valor = float(input("\nValor da conversao: "))

    conn.insert_conversion(nome, valor)

# Menu de operações
def operation():
    opt = int(input("\n[1] Cadastrar nova operação\n[2] Mostrar todas operações\n[3] Atualizar uma operação\n[4] Deletar uma operação\n[5] Mostrar o valor total das operações\n[6] Mostrar o valor total das taxas\n"))
    os.system('cls||clear')
    if(opt == 1):
        op = new_operation()
        conn.insert_operation(op)
        menu()
    elif(opt == 2):
        opt = int(input("\n[1] Sem Filtro\n[2] Filtrar por cliente\n[3] Filtrar por data\n"))
        if(opt==1):
            res = conn.getAll()
        elif(opt==2):
            res = conn.getAll_orderBy_client()
        elif(opt==3):
            res = conn.getAll_orderBy_date()
        n = 1
        for i in res:
            print("ID: ", n, "| cliente: ", i[0],"| moeda de origem: ", i[1],"| moeda de destino: ", i[2],"| data: ", i[3],"| valor a ser convertido: ", i[4],"| valor convertido: ", i[5],"| taxa de conversão: ", i[6],"| valor descontado a taxa: ", i[7])
            n+=1
        menu()
    elif(opt == 3):
        id = input("\nId da operação a ser atualizada: ")
        op = new_operation()
        conn.update(id, op)
    elif(opt == 4):
        id = input("\nId da operação a ser removida: ")
        conn.delete(id)
        menu()
    elif(opt == 5):
        print(conn.get_valor_total())
        menu()
    elif(opt == 6):
        print(conn.get_valor_total_taxas())
        menu()
    else:
        print("Opção inválida")
        operation()

# Menu de conversão
def conversion():
    opt = int(input("\n[1] Cadastrar nova conversão\n[2] Mostrar todos valores de conversão\n[3] Deletar um valor de conversão\n"))
    os.system('cls||clear')
    if(opt == 1):
        new_conversion()
        menu()
    elif(opt == 2):
        conversoes = conn.getAll_conversion()
        i=1
        for c in conversoes:
            print(i,c)
            i+=1
    elif(opt == 3):
        id = input("\nId da conversão a ser removida: ")
        conn.delete_conversion(id)
    else:
        print("Opção inválida")
        conversion()

# Menu inicial
def menu():
    opt = int(input("\nEscolha uma opção:\n[1] - Operações\n[2] - Conversões\n"))
    os.system('cls||clear')
    if(opt == 1):
        operation()
    elif(opt == 2):
        conversion()
    else:
        print("Opção inválida")
        menu()

# Iniciador do projeto
if __name__=='__main__':
    try:
        menu()
    except KeyboardInterrupt:
        print('Saindo...')
        os._exit(0)