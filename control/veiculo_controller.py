from dao.veiculo_dao import VeiculoDAO
from model.Veiculo import *
from model.VeiculoFactory import VeiculoFactory

class Veiculocontroller():
    def __init__(self):
        self.veiculo_dao = VeiculoDAO()
    
    def salvar_veiculo(self, placa_str : str, tipo_str : str, categoria_str : str, taxa_str : str):
        if not placa_str or not tipo_str or not categoria_str or not taxa_str:
            return False, "Preencha todos os campos !"
        
        try:
            taxa_num = float(taxa_str.replace(',','.'))
            if taxa_num <= 0:
                return False, "A taxa diaria deeve ser um valor positivo"
            
            veiculo_existente = self.veicuo_dao.buscar_por_placa(placa_str)
            if veiculo_existente:
                return False, f"Veiculo com placa {placa_str} já está cadastrado"
            
            categoria_enum = Categoria[categoria_str.upper()]

            novo_veiculo = VeiculoFactory.criar_veiculo()

            # tem que terminar aqui, com base no q ela postar no class



        except KeyError:
            return False, "Categoria inválida. Use ECONOMICO  ou EXECUTIVO."
        except ValueError as e2:
            return False, f"Valor númerico inválido. Erro: {e2}"
        except Exception as e3:
            return False, f"Erro: {e3}"