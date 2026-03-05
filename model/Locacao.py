from datetime import date, time, datetime, timedelta
from .Veiculo import Veiculo

class Locacao:
    def __init__(self, data_inicio=None, data_fim=None, veiculo=None):
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.veiculo = veiculo

    @property
    def data_inicio(self):
        return self.__data_inicio

    @data_inicio.setter
    def data_inicio(self, data_ini):
        # Chama a validação, que já retorna o valor convertido (ou None)
        self.__data_inicio = self.valida_data(data_ini)

    @property
    def data_fim(self):
        return self.__data_fim

    @data_fim.setter
    def data_fim(self, data_f):
        self.__data_fim = self.valida_data(data_f)
    
    @property
    def veiculo(self):
        return self.__veiculo
    
    @veiculo.setter
    def veiculo(self, obj):
        # Permite None (para inicialização vazia) OU um objeto Veiculo
        if obj is None or isinstance(obj, Veiculo):
            self.__veiculo = obj
        else:
            raise TypeError("O valor informado deve ser um objeto do tipo Veículo!")

    def calcular_valor_locacao(self):
        pass
        #IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
        #IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII

    def valida_data(self, data_recebida):
        # 1. Se for nulo, apenas retorna nulo
        if data_recebida is None:
            return None
        
        # 2. BÔNUS: Se a pessoa já passou um objeto 'date' pronto (sem ser string), a gente só aceita e retorna ele!
        if isinstance(data_recebida, date):
            return data_recebida
            
        # 3. Se for string, tenta converter
        try:
            temporario = datetime.strptime(data_recebida, "%d-%m-%Y")
            return temporario.date() # Retorna apenas a parte da data (ano, mês, dia)
        except ValueError:
            raise ValueError(
                f"ERRO: Data '{data_recebida}' em formato inválido. Use DD-MM-YYYY."
            )