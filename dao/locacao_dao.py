import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dao.db_config import DatabaseConfig
from dao.generic_dao import GenericDAO
from model.Locacao import Locacao
from model.StatusLocacao import StatusLocacao
from dao.veiculo_dao import VeiculoDAO
from model.LocacaoStrategy import *

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
                (vei_placa, loc_data_inicio, loc_data_fim, loc_status, loc_valor_total, loc_estrategia) 
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING loc_id;
            """
            placa = objeto_locacao.veiculo.placa if hasattr(objeto_locacao.veiculo, 'placa') else objeto_locacao.veiculo
            
            valores = (
                placa,
                objeto_locacao.data_inicio, 
                objeto_locacao.data_fim, 
                objeto_locacao.status.value, 
                objeto_locacao.valor_locacao,
                objeto_locacao.estrategia.__class__.__name__
            )
            cursor.execute(query, valores)

            id_gerado = cursor.fetchone()[0]
            objeto_locacao.id = id_gerado
            
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
            query = "SELECT loc_id, vei_placa, loc_data_inicio, loc_data_fim, loc_status, loc_valor_total, loc_estrategia FROM tb_locacoes;"
            cursor.execute(query)
            linhas = cursor.fetchall()
            locacoes = []

            for cada_linha in linhas: 
                objeto_veiculo = v_dao.buscar_por_placa(cada_linha[1])

                try:
                    status_enum = StatusLocacao(cada_linha[4])
                except ValueError:
                    status_enum = StatusLocacao[cada_linha[4].upper()]

                estrategia_de_pagamento_obj = cada_linha[6] 
                if estrategia_de_pagamento_obj == "CalculoVIPStrategy":
                    estrategia_de_pagamento_obj = CalculoVIPStrategy()
                else:
                    estrategia_de_pagamento_obj = CalculoPadraoStrategy()

                obj = Locacao(
                    id = cada_linha[0],
                    data_inicio=cada_linha[2], 
                    data_fim=cada_linha[3], 
                    veiculo=objeto_veiculo,
                    status=status_enum,
                    estrategia = estrategia_de_pagamento_obj
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


    def buscar_por_codigo(self, id: str):
        if not self.conexao:
            return None
        try:
            cursor = self.conexao.cursor()
            query = "SELECT loc_id, vei_placa, loc_data_inicio, loc_data_fim, loc_status, loc_valor_total, loc_estrategia FROM tb_locacoes where loc_id = %s;"
            cursor.execute(query, (id,))
            linha = cursor.fetchone()

            if linha:
                v_dao = VeiculoDAO()
                objeto_veiculo = v_dao.buscar_por_placa(linha[1])

                estrategia_str = linha[6] 
                if estrategia_str == "CalculoVIPStrategy":
                    estrategia_obj = CalculoVIPStrategy()
                else:
                    estrategia_obj = CalculoPadraoStrategy()

                try:
                    locacao_status = StatusLocacao(linha[4])
                except ValueError:
                    locacao_status = StatusLocacao[linha[4].upper()]

                locacao_encontrada = Locacao(
                    id = linha[0], 
                    data_inicio= linha[2],
                    data_fim= linha[3],
                    veiculo= objeto_veiculo,
                    status = locacao_status,
                    estrategia= estrategia_obj
                )
                locacao_encontrada.valor_locacao = float(linha[5]) if linha[5] else 0.0
                
                return locacao_encontrada
            
            return None

        except Exception as e:
            print(f"Erro ao buscar locação no BD: {e}")
            return None
        finally:
            if cursor: cursor.close()

    def atualizar(self, objeto_locacao):
        if not self.conexao:
            return False, "Sem conexão com o Banco de Dados" 
        
        try:
            cursor = self.conexao.cursor()
            query = """
                UPDATE tb_locacoes SET
                vei_placa = %s,
                loc_data_inicio = %s,
                loc_data_fim = %s,
                loc_status = %s,
                loc_valor_total = %s,
                loc_estrategia = %s
                WHERE loc_id = %s;
            """
            
            valores = (
                objeto_locacao.veiculo.placa if hasattr(objeto_locacao.veiculo, 'placa') else objeto_locacao.veiculo,
                objeto_locacao.data_inicio, 
                objeto_locacao.data_fim,
                objeto_locacao.status.value,
                objeto_locacao.valor_locacao,
                objeto_locacao.estrategia.__class__.__name__, 
                objeto_locacao.id
            )

            cursor.execute(query, valores)
            self.conexao.commit()

            if cursor.rowcount > 0:
                return True, f"Locação #{objeto_locacao.id} atualizada com sucesso!"
            else:
                return False, "Locação não encontrada para atualização."
            
        except Exception as e:
            if self.conexao:
                self.conexao.rollback()
            return False, f"Erro ao atualizar: {e}"
        
        finally:
            if cursor:
                cursor.close()


    def remover(self, id_objeto):
        if not self.conexao:
            return False, "Sem conexão com o banco."
        
        cursor = None
        try:
            cursor = self.conexao.cursor()
            
            query = "DELETE FROM tb_locacoes WHERE loc_id = %s;"
            
            cursor.execute(query, (id_objeto,))
            
            if cursor.rowcount > 0:
                self.conexao.commit()
                return True, f"Locação #{id_objeto} removida com sucesso!"
            else:
                return False, "Locação não encontrada no banco de dados."
                
        except Exception as e:
            if self.conexao:
                self.conexao.rollback()
            return False, f"Erro ao remover: {e}"
        
        finally:
            if cursor:
                cursor.close()