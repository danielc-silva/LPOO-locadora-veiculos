import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime, date
from model.Locacao import Locacao
from model.Veiculo import Veiculo
from model.StatusLocacao import StatusLocacao
from dao.veiculo_dao import VeiculoDAO
from dao.locacao_dao import LocacaoDAO
from model.LocacaoStrategy import *

class LocacaoController:
    def __init__(self):
        self.locacao_dao = LocacaoDAO()
        self.veiculo_dao = VeiculoDAO()


    def salvar_locacoes(self, placa_str: str, locacao_inicio_str: str, locacao_fim_str: str, status_str: str, estrategia_str: str):
        if not all([placa_str, locacao_inicio_str, locacao_fim_str, status_str, estrategia_str]):
            return False, "Preencha todos os campos!"

        if status_str == "Selecione o status":
            return False, "Selecione um status válido!"
        
        if estrategia_str.upper() == "VIP":
            estrategia_recebida = CalculoVIPStrategy()
        else:
            estrategia_recebida = CalculoPadraoStrategy()

        try:
            data_ini = datetime.strptime(locacao_inicio_str.strip(), "%d/%m/%Y").date()
            data_fimm = datetime.strptime(locacao_fim_str.strip(), "%d/%m/%Y").date()

            veiculo_existente = self.veiculo_dao.buscar_por_placa(placa_str.strip().upper())
            if not veiculo_existente:
                return False, f"Veículo com placa {placa_str} não existe no sistema!"
            
            status_enum = StatusLocacao[status_str.upper().strip()]

            nova_locacao = Locacao(
                data_inicio=data_ini,
                data_fim=data_fimm,
                veiculo=veiculo_existente,
                status=status_enum,
                estrategia=estrategia_recebida
            )

            try:
                nova_locacao.valor_locacao = nova_locacao.calcular_valor_locacao()
            except Exception:

                nova_locacao.valor_locacao = 0.0

            sucesso, msg = self.locacao_dao.salvar(nova_locacao)
            return sucesso, msg

        except ValueError:
            return False, "Formato de data inválido! Use DD/MM/AAAA."
        except KeyError:
            return False, f"Status '{status_str}' não reconhecido pelo sistema."
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


    def remover_locacao(self, codigo: str):
        if not codigo:
            return False,"Código da locação não informado."
        try:
            return self.locacao_dao.remover(codigo.strip())
        
        except Exception as e:
            return False, f"Erro inesperado: {e}"
        
    def editar_locacao(self, codigo: str, placa: str, data_inii: str, data_fim: str, loc_status: str, valor_loc: str, estrategia_pgt: str):
        if not all([codigo, placa, data_inii, data_fim, loc_status, estrategia_pgt]):
            return False, "Preencha todos os campos obrigatórios!"
        
        try:

            data_ini = datetime.strptime(data_inii.strip(), "%d/%m/%Y").date()
            data_fimm = datetime.strptime(data_fim.strip(), "%d/%m/%Y").date()

            veiculo_existente = self.veiculo_dao.buscar_por_placa(placa.strip().upper())
            if not veiculo_existente:
                return False, f"Veículo com placa {placa} não encontrado!"

            status_enum = StatusLocacao[loc_status.upper().strip()]

            if estrategia_pgt.upper() == "VIP":
                estrategia_recebida = CalculoVIPStrategy()
            else:
                estrategia_recebida = CalculoPadraoStrategy()

            locacao_editada = Locacao(
                data_inicio=data_ini,
                data_fim=data_fimm,
                veiculo=veiculo_existente,
                status=status_enum,
                estrategia=estrategia_recebida
            )
            locacao_editada.id = int(codigo) 

            try:
                locacao_editada.valor_locacao = locacao_editada.calcular_valor_locacao()
            except Exception:
                locacao_editada.valor_locacao = float(valor_loc.replace(',', '.'))

            sucesso, msg = self.locacao_dao.atualizar(locacao_editada)
            return sucesso, msg
        
        except ValueError:
            return False, "Erro nos dados: Verifique o formato de data (DD/MM/AAAA) e valores numéricos."
        except KeyError:
            return False, f"Status '{loc_status}' é inválido."
        except Exception as e:
            return False, f"Erro inesperado no Controller: {e}"

        
        


        
        