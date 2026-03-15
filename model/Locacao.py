from datetime import date, time, datetime, timedelta
from .Veiculo import Veiculo
from .LocacaoStrategy import CalculoVIPStrategy, CalculoPadraoStrategy, CalculoLocacaoStrategy

class Locacao:
    def __init__(self, data_inicio=None, data_fim=None, veiculo=Veiculo, estrategia = CalculoPadraoStrategy()):
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.veiculo = veiculo
        self.valor_locacao = 0.00
        self.estrategia = estrategia

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
            if obj is not None:
                obj.tentar_alugar()
            self.__veiculo = obj
        else:
            raise TypeError("O valor informado deve ser um objeto do tipo Veículo!")

    def calcular_valor_locacao(self):
        if (self.data_inicio == self.data_fim):
            diferenca_de_dias = 1
        else:
            diferenca_de_dias = (self.data_fim - self.data_inicio).days
        #valor_final_locacao = (diferenca_de_dias * self.veiculo.taxa_diaria) + self.veiculo.valor_seguro
        #self.valor_locacao = valor_final_locacao
        self.valor_locacao = self.estrategia.calcuar_diarias(self.veiculo, diferenca_de_dias)
    
    def registrar_devolucao_de_veiculo (self, data_devolucao):
        self.data_fim = data_devolucao
        if not(self.data_inicio <= self.data_fim):
            print (f'A data está incorreta!\nA data de devolução deve ser maior ou igual a data de início: [{self.data_inicio}].')
            self.data_fim = None
            return
        else:
            self.calcular_valor_locacao()

    def valida_data(self, data_recebida):
        if data_recebida is None:
            return None
        if isinstance(data_recebida, date):
            return data_recebida
        try:
            temporario = datetime.strptime(data_recebida, "%d-%m-%Y")
            return temporario.date()
        except ValueError:
            raise ValueError(
                f"ERRO: Data '{data_recebida}' em formato inválido. Use DD-MM-YYYY."
            )
        

    def __str__(self):
        mostrar = "==================================="
        mostrar += f"\nMostrando dados da Locação"
        mostrar += f"\nData inicio: {self.data_inicio}"
        if (self.data_fim is None):
            mostrar += f"\nData fim: Veículo ainda se encontra locado."
        else:
            mostrar += f"\nData fim = {self.data_fim}"
        mostrar += f"\nPlaca veículo Locado: {self.veiculo.placa}"
        mostrar += f"\nValor locação: {self.valor_locacao}"
        mostrar += "\n==================================="
        return  mostrar