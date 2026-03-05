from abc import ABC, abstractmethod
from .Categoria import Categoria
from .ExcecoesPersonalizadas import PlacaInvalidaError

class Veiculo (ABC):
    def __init__(self, placa = None, taxa_diaria = 0.00, categoria = Categoria.ECONOMICO):
        self.placa = placa
        self.categoria = categoria
        self.taxa_diaria = taxa_diaria

    @property
    def placa(self):
        return self.__placa
    
    @placa.setter
    def placa(self, valor_placa):
        if valor_placa is None:
            self.__placa = None
            return    
        placa_limpa = self.valida_placa(valor_placa)
        self.__placa = placa_limpa
    
    def valida_placa(self, placa):
        placa = placa.strip().replace("-", "").upper()
        if len(placa) != 7:
            raise PlacaInvalidaError("Placa inválida! Deve conter 7 caracteres.")
        # Verifica se começa com 3 letras
        if not placa[0:3].isalpha():
            raise PlacaInvalidaError("Placa inválida! Os três primeiros caracteres devem ser letras.")
        # Formato antigo: ABC1234
        if placa[3:7].isdigit():
            print(f"Placa {placa} válida (modelo antigo)")
            return True
        # Formato Mercosul: ABC1D23
        if placa[3].isdigit() and placa[4].isalpha() and placa[5:7].isdigit():
            print(f"Placa {placa} válida (Mercosul)")
            return placa
        raise PlacaInvalidaError("Formato de placa inválido!")

    @property
    def taxa_diaria(self):
        return self.__taxa_diaria
    
    @taxa_diaria.setter
    def taxa_diaria (self, taxa_diaria):
        self.__taxa_diaria = taxa_diaria

    def __str__(self):
        return f"Carro(placa='{self.placa}', categoria='{self.categoria}', taxa_diaria={self.taxa_diaria})"
    


    


    