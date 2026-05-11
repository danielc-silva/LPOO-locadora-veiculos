from datetime import date, time, datetime, timedelta
from .Veiculo import Veiculo
from .LocacaoStrategy import CalculoVIPStrategy, CalculoPadraoStrategy, CalculoLocacaoStrategy
from .StatusLocacao import StatusLocacao

class Locacao:
    def __init__(self, data_inicio=None, data_fim=None, veiculo=Veiculo, estrategia = CalculoPadraoStrategy(), status = StatusLocacao.RESERVADO, id = None):
        self.id = id
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.veiculo = veiculo
        self.valor_locacao = 0.00
        self.estrategia = estrategia
        self.status = status

    @property
    def status(self):
        return self.__status
        
    @status.setter
    def status(self, valor):
        if isinstance(valor, StatusLocacao):
            self.__status = valor 
            
        elif isinstance(valor, str):
            texto_limpo = valor.strip().upper()
            if texto_limpo == "RESERVADO":
                self.__status = StatusLocacao.RESERVADO
            elif texto_limpo == "LOCADO":
                self.__status = StatusLocacao.LOCADO
            elif texto_limpo == "DEVOLVIDO":
                self.__status = StatusLocacao.DEVOLVIDO
            elif texto_limpo == "CANCELADO":
                self.__status = StatusLocacao.CANCELADO
            else:
                raise ValueError(f"Erro: O status '{valor}' é inválido.")
        else:
            raise TypeError("Erro: O formato do status é inválido.")

    @property
    def data_inicio(self):
        return self.__data_inicio

    @data_inicio.setter
    def data_inicio(self, data_ini):
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
        if obj is None or isinstance(obj, Veiculo):
            self.__veiculo = obj
        else:
            raise TypeError("O valor informado deve ser um objeto do tipo Veículo!")

    def calcular_valor_locacao(self):
        if self.data_fim is None:
            raise ValueError("Impossível calcular o valor, a data de devolução não foi definida.")

        delta = self.data_fim - self.data_inicio
        dias_brutos = delta.days
        
        diferenca_de_dias = dias_brutos if dias_brutos > 0 else 1
                
        self.valor_locacao = self.estrategia.calcuar_diarias(self.veiculo, diferenca_de_dias)
        
        return self.valor_locacao
    
    def registrar_devolucao_de_veiculo(self, data_devolucao):
        self.data_fim = data_devolucao
        if not (self.data_inicio <= self.data_fim):
            self.data_fim = None
            raise ValueError(f"A data está incorreta! A data de devolução deve ser maior ou igual a data de início: [{self.data_inicio}].")
        else:
            self.valor_locacao = self.calcular_valor_locacao()
            if self.veiculo is not None:
                self.veiculo.tentar_devolver()

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
    def exibir_dados(self):
        mostrar = f"\nMostrando dados da Locação"
        mostrar += f"\nCódigo: {self.id}"
        mostrar += f"\nData inicio: {self.data_inicio}"
        mostrar += f"\nData fim: {self.data_fim}"
        mostrar += f"\nPlaca veículo: {self.veiculo.placa}"
        mostrar += f"\nStatus: {self.status.value.upper()}"
        mostrar += f"\nValor locação: {self.valor_locacao}"
        return  mostrar
    
    def exibir_previsao(self):
        mostrar = f"\nMostrando dados da Locação"
        mostrar += f"\nCódigo: {self.id}"
        mostrar += f"\nData inicio: {self.data_inicio}"
        mostrar += f"\nData fim prevista: {self.data_fim}"
        mostrar += f"\nPlaca veículo: {self.veiculo.placa}"
        mostrar += f"\nStatus: {self.status.value.upper()}"
        mostrar += f"\nValor estimado: {self.valor_locacao}"
        return  mostrar
    
    def exibir_basico(self):
        mostrar = f"\nMostrando dados da Locação"
        mostrar += f"\nCódigo: {self.id}"
        mostrar += f"\nData inicio: {self.data_inicio}"
        mostrar += f"\nPlaca veículo: {self.veiculo.placa}"
        mostrar += f"\nStatus: {self.status.value.upper()}"
        return  mostrar

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