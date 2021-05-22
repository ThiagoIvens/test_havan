
# Classe para tratamento de dados de forma mais simplificada
class Operation:
    def __init__(self, name, mOrigem, mDestino, data, valor, vConvertido, taxa, valorDescTaxa):
        self.name = name
        self.mOrigem = mOrigem
        self.mDestino = mDestino
        self.data = data
        self.valor = valor
        self.vConvertido = vConvertido
        self.taxa = taxa
        self.valorDescTaxa = valorDescTaxa