from dao.veiculo_dao import VeiculoDAO
from model.Veiculo import *
from model.VeiculoFactory import VeiculoFactory

class VeiculoController:
    def __init__(self):
        self.veiculo_dao = VeiculoDAO()
    
    def salvar_veiculo(self, placa_str: str, tipo_str: str, categoria_str: str, taxa_str: str):
        if not placa_str or not tipo_str or not categoria_str or not taxa_str:
            return False, "Preencha todos os campos!"
        
        if tipo_str == "Selecione o Tipo" or categoria_str == "Selecione a Categoria":
            return False, "Selecione um Tipo e uma Categoria válidos."
        
        try:
            taxa_num = float(taxa_str.replace(',', '.'))
            if taxa_num <= 0:
                return False, "A taxa diária deve ser um valor positivo."
            
            veiculo_existente = self.veiculo_dao.buscar_por_placa(placa_str.strip().upper())
            if veiculo_existente:
                return False, f"Veículo com placa {placa_str} já está cadastrado!"
            
            categoria_enum = Categoria[categoria_str.upper()]

            novo_veiculo = VeiculoFactory.criar_veiculo(
                tipo_veiculo=tipo_str,
                placa=placa_str.strip().upper(),
                categoria=categoria_enum,
                taxa_diaria=taxa_num
            )

            sucesso, msg = self.veiculo_dao.salvar(novo_veiculo)
            return sucesso, msg

        except KeyError:
            return False, "Categoria inválida. Use ECONOMICO, EXECUTIVO ou LUXO."
        except ValueError as e2:
            return False, f"Valor numérico inválido. Erro: {e2}"
        except Exception as e3:
            return False, f"Erro inesperado: {e3}"

    def atualizar_veiculo(self, placa_str: str, tipo_str: str, categoria_str: str, taxa_str: str):
        # Validação básica
        if not placa_str or not tipo_str or not categoria_str or not taxa_str:
            return False, "Preencha todos os campos!"
        
        try:
            taxa_num = float(taxa_str.replace(',', '.'))
            if taxa_num <= 0:
                return False, "A taxa diária deve ser um valor positivo."
            
            veiculo_existente = self.veiculo_dao.buscar_por_placa(placa_str.strip().upper())
            if not veiculo_existente:
                return False, f"Veículo com placa {placa_str} não foi encontrado."
            
            categoria_enum = Categoria[categoria_str.upper()]
            
            veiculo_atualizado = VeiculoFactory.criar_veiculo(
                tipo_veiculo=tipo_str,
                placa=placa_str.strip().upper(),
                categoria=categoria_enum,
                taxa_diaria=taxa_num
            )
        
            sucesso, msg = self.veiculo_dao.atualizar(veiculo_atualizado)
            return sucesso, msg

        except KeyError:
            return False, "Categoria inválida. Use ECONOMICO, EXECUTIVO ou LUXO."
        except ValueError as e2:
            return False, f"Valor numérico inválido. Erro: {e2}"
        except Exception as e3:
            return False, f"Erro inesperado: {e3}"

    def listar_veiculos(self):
        try:
            return self.veiculo_dao.listar_todos()
        except Exception as e:
            print(f"Erro ao listar veículos: {e}")
            return []

    def buscar_por_placa(self, placa: str):
        try:
            return self.veiculo_dao.buscar_por_placa(placa.strip().upper())
        except Exception as e:
            print(f"Erro ao buscar veículo: {e}")
            return None

    def remover_veiculo(self, placa: str):
        if not placa:
            return False, "Placa não informada."
        try:
            return self.veiculo_dao.remover(placa.strip().upper())
        except Exception as e:
            return False, f"Erro inesperado: {e}"