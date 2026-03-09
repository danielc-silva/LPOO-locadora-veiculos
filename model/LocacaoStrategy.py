from abc import ABC, abstractmethod
from .Veiculo import Veiculo

class CalculoLocacaoStrategy (ABC):
    @abstractmethod
    def calcuar_diarias(self, veiculo : Veiculo, dias : int) -> float:
        pass

class CalculoPadraoStrategy (CalculoLocacaoStrategy):
    def calcuar_diarias(self, veiculo, dias):
        valor_diarias = veiculo.taxa_diaria * dias

        return (valor_diarias + veiculo.valor_seguro)
    
class CalculoVIPStrategy (CalculoLocacaoStrategy):
    def calcuar_diarias(self, veiculo: Veiculo, dias):
        valor_diarias = veiculo.taxa_diaria * dias
        return ((valor_diarias * 0.8) + veiculo.valor_seguro)