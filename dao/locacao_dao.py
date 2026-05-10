import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dao.db_config import DatabaseConfig
from dao.generic_dao import GenericDAO
from model.Locacao import Locacao
from model.StatusLocacao import StatusLocacao
from dao.veiculo_dao import VeiculoDAO # Importado corretamente

class LocacaoDAO(GenericDAO):
    def __init__(self):
        self.conexao = DatabaseConfig.get_connection()

    def salvar(self, objeto_locacao):
        if not self.conexao:
            raise Exception("Sem conexão com o banco de dados")
        
        try:
            cursor = self.conexao.cursor()
            query = """
                INSERT INTO tb_locacoes 
                (vei_placa, loc_data_inicio, loc_data_fim, loc_status, loc_valor_total) 
                VALUES (%s, %s, %s, %s, %s)
            """
            placa = objeto_locacao.veiculo.placa if hasattr(objeto_locacao.veiculo, 'placa') else objeto_locacao.veiculo
            
            valores = (
                placa,
                objeto_locacao.data_inicio, 
                objeto_locacao.data_fim, 
                objeto_locacao.status.value, 
                objeto_locacao.valor_locacao
            )
            
            cursor.execute(query, valores)
            self.conexao.commit()
            return True, "Locação salva com sucesso"
        except Exception as e:
            if self.conexao: self.conexao.rollback()
            return False, f"Erro: {e}"
        finally:
            if cursor: cursor.close()

    def listar_todos(self):
        if not self.conexao:
            return []

        v_dao = VeiculoDAO()

        try:
            cursor = self.conexao.cursor()
            query = "SELECT loc_id, vei_placa, loc_data_inicio, loc_data_fim, loc_status, loc_valor_total FROM tb_locacoes;"
            cursor.execute(query)
            linhas = cursor.fetchall()
            locacoes = []

            for cada_linha in linhas: 
                objeto_veiculo = v_dao.buscar_por_placa(cada_linha[1])

                try:
                    status_enum = StatusLocacao(cada_linha[4])
                except ValueError:
                    status_enum = StatusLocacao[cada_linha[4].upper()]

                obj = Locacao(
                    data_inicio=cada_linha[2], 
                    data_fim=cada_linha[3], 
                    veiculo=objeto_veiculo,
                    status=status_enum
                )
                
                obj.id = cada_linha[0] 
                obj.valor_locacao = float(cada_linha[5]) if cada_linha[5] else 0.0
                
                locacoes.append(obj)

            return locacoes

        except Exception as e:
            print(f"Erro ao buscar locações no DAO: {e}")
            return []
        finally:
            if cursor: cursor.close()

    def remover(self, id_objeto):
        pass

    def atualizar(self, objeto):
        pass