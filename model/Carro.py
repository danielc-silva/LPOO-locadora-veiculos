from .Veiculo import Veiculo
from .Categoria import Categoria


class Carro (Veiculo):
     def __init__(self, placa = None, taxa_diaria = 0.00, categoria = None, valor_seguro = 50.00):
        super().__init__(placa, taxa_diaria, categoria)
        self.__valor_seguro = valor_seguro