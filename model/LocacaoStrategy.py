from abc import ABC, abstractmethod
from .Veiculo import Veiculo

class CalculoLocacaoStrategy (ABC):
    @abstractmethod
    def calcuar_diarias(self, veiculo : Veiculo, dias : int) -> float:
        pass

class CalculoPadraoStrategy(CalculoLocacaoStrategy):
    def calcuar_diarias(self, veiculo, dias):
        taxa = float(veiculo.taxa_diaria)
        seguro = float(veiculo.valor_seguro)
        
        valor_diarias = taxa * dias
        return valor_diarias + seguro
    
class CalculoVIPStrategy(CalculoLocacaoStrategy):
    def calcuar_diarias(self, veiculo, dias):
        taxa = float(veiculo.taxa_diaria)
        seguro = float(veiculo.valor_seguro)
        
        valor_diarias = taxa * dias
        return (valor_diarias * 0.8) + seguro