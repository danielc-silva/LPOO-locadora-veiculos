import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime, date
from model.Locacao import Locacao
from model.Veiculo import Veiculo
from model.StatusLocacao import StatusLocacao
from dao.veiculo_dao import VeiculoDAO
from dao.locacao_dao import LocacaoDAO

class LocacaoController:
    def __init__(self):
        self.locacao_dao = LocacaoDAO()
        self.veiculo_dao = VeiculoDAO()


    def salvar_locacoes (self, placa_str:  str, locacao_inicio_str: str, locacao_fim_str: str, status_str: str):
        if not placa_str or not locacao_inicio_str or not locacao_fim_str or not status_str:
            return False, "Preencha todos os campos!"

        if status_str == "Selecione o status":
            return False, "Selecione um status válido!"

        try:
            data_ini = datetime.strptime(locacao_inicio_str.strip(), "%d/%m/%Y").date()
            data_fimm = datetime.strptime(locacao_fim_str.strip(), "%d/%m/%Y").date()

            veiculo_existente = self.veiculo_dao.buscar_por_placa (placa_str.strip().upper())
            if not veiculo_existente:
                return False, f"Veículo com placa {placa_str} não existe no sistema!"
            
            status_enum = StatusLocacao[status_str.upper()]

            nova_locacao = Locacao(
                data_inicio = data_ini,
                data_fim = data_fimm,
                veiculo = veiculo_existente,
                status = status_enum
            )
            nova_locacao.valor_locacao = nova_locacao.calcular_valor_locacao()
            sucesso, msg = self.locacao_dao.salvar(nova_locacao)
            return sucesso, msg

        except KeyError:
            return False, "Status inválido!"
        except Exception as e:
            return False, f"Erro inesperado: {e}"

    def listar_locacoes(self):
        try:
            return self.locacao_dao.listar_todos()
        except Exception as e:
            return [], f"Erro ao listar locações: {e}"


    def buscar_por_codigo (self, codigo_str: str):
        try:
            return self.locacao_dao.buscar_por_codigo(codigo_str.strip())
        except Exception as e :
            print (f"Erro ao buscar locação: {e}")  


    def locar_veiculo (self, codigo_loc_str):
        locacao_existente = self.locacao_dao.buscar_por_codigo(codigo_loc_str.strip())
        if not locacao_existente:
            return False, f"Locação de código {codigo_loc_str} não encontrada."
        
        if locacao_existente.status == StatusLocacao.LOCADO:
            return False, f"Veículo com placa {locacao_existente.veiculo.placa} já está locado."

        hoje = date.today()

        if locacao_existente.data_inicio != hoje:
            locacao_existente.data_inicio = hoje

        locacao_existente.status = StatusLocacao.LOCADO
        locacao_existente.valor_locacao = locacao_existente.calcular_valor_locacao()

        sucesso, msg = self.locacao_dao.atualizar(locacao_existente)
        return sucesso, msg

    def devolver_veiculo(self, codigo_loc_str):
        locacao = self.locacao_dao.buscar_por_codigo(codigo_loc_str.strip())
        
        if not locacao:
            return False, f"Locação #{codigo_loc_str} não encontrada."

        if locacao.status != StatusLocacao.LOCADO:
            return False, "O veículo não consta como 'LOCADO' para este código."
        try:
            hoje = date.today()
            locacao.status = StatusLocacao.DEVOLVIDO
            locacao.data_fim = hoje
            locacao.valor_locacao = locacao.calcular_valor_locacao()

            sucesso, msg = self.locacao_dao.atualizar(locacao)
            
            if sucesso:
                return True, f"Veículo da locação #{codigo_loc_str} devolvido com sucesso!"
            return False, msg

        except Exception as e:
            return False, f"Falha ao processar devolução: {e}"
        
    def calcelar_reserva (self, codigo_loc_str):
        locacao_existente = self.locacao_dao.buscar_por_codigo(codigo_loc_str.strip())
        if not locacao_existente:
            return False, f"Locação de código {codigo_loc_str} não encontrada."
        
        if locacao_existente.status != StatusLocacao.RESERVADO:
            return False, "Apenas veículos reservados podem ser cancelados."
        
        try:
            locacao_existente.status = StatusLocacao.CANCELADO

            sucesso, msg = self.locacao_dao.atualizar(locacao_existente)
            if sucesso:
                return True, f"Reserva {codigo_loc_str} cancelada com sucesso!"
            
            return sucesso, msg
        except Exception as e:
            return False, f"Erro ao processar cancelamento: {e}"

        

        
        


        
        