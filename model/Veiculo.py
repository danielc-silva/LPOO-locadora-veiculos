from abc import ABC, abstractmethod
from .Categoria import Categoria
from .ExcecoesPersonalizadas import PlacaInvalidaError
from .Estados_veiculo import DisponivelState

class Veiculo (ABC):
    def __init__(self, placa = None, taxa_diaria = 0.00, categoria = Categoria.ECONOMICO, valor_seguro = 0.00):
        self.placa = placa
        self.categoria = categoria
        self.taxa_diaria = taxa_diaria
        self.valor_seguro = valor_seguro
        self.estado_atual = DisponivelState (self)

    @property
    def estado_atual(self):
        return self.__estado_atual

    @estado_atual.setter
    def estado_atual(self, novo_estado):
        self.__estado_atual = novo_estado

    # métodos do state

    def tentar_alugar(self):
        self.estado_atual.alugar()

    def tentar_devolver(self):
        self.estado_atual.devolver()

    def reter_na_frota_pra_conserto(self):
        self.estado_atual.enviar_manutencao()

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
            #print(f"Placa {placa} válida (modelo antigo)")
            return placa
        # Formato Mercosul: ABC1D23
        if placa[3].isdigit() and placa[4].isalpha() and placa[5:7].isdigit():
            #print(f"Placa {placa} válida (Mercosul)")
            return placa
        raise PlacaInvalidaError("Formato de placa inválido!")

    @property
    def taxa_diaria(self):
        return self.__taxa_diaria
    
    @taxa_diaria.setter
    def taxa_diaria (self, taxa_diaria):
        self.__taxa_diaria = taxa_diaria

    @property
    def valor_seguro (self):
        return self.__valor_seguro
      
    @valor_seguro.setter
    def valor_seguro (self, valor):
        if not isinstance(valor, (int, float)):
            raise TypeError("Erro: O valor do seguro deve ser numérico (inteiro ou decimal).")
        if valor < 0:
            raise ValueError("Erro: O valor do seguro não pode ser negativo.")
        self.__valor_seguro = float(valor)

    def __str__(self):
        nome_classe_filha_de_veiculo = self.__class__.__name__
        nome_estado = self.estado_atual.__class__.__name__
        return f"{nome_classe_filha_de_veiculo} (placa='{self.placa}', categoria='{self.categoria}', taxa_diaria={self.taxa_diaria}, valor_seguro={self.valor_seguro}, estado='{nome_estado}')"
