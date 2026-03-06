from .Veiculo import Veiculo
from .Categoria import Categoria


class Motorhome (Veiculo):
     def __init__(self, placa = None, taxa_diaria = 0.00, categoria = None, valor_seguro = 120.00):
        super().__init__(placa, taxa_diaria, categoria, valor_seguro)