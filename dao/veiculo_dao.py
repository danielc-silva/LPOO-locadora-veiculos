import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.Veiculo import *
from model.VeiculoFactory import VeiculoFactory
from dao.db_config import DatabaseConfig
from dao.generic_dao import GenericDAO

class VeiculoDAO (GenericDAO):
    def __init__(self):
       self.conexao = DatabaseConfig.get_connection()

    def salvar(self, objeto_veiculo):
        if not self.conexao:
            raise Exception("Sem conexão com o Banco de Dados")
        
        try:
            cursor = self.conexao.cursor()
            query = "INSERT INTO tb_veiculos (vei_placa, vei_categoria, vei_taxa_diaria, vei_estado_atual, vei_tipo) VALUES (%s, %s, %s, %s, %s)"            
            cursor.execute(query, (objeto_veiculo.placa, objeto_veiculo.categoria.value, objeto_veiculo.taxa_diaria, objeto_veiculo.estado_atual.__class__.__name__, objeto_veiculo.__class__.__name__))            
            self.conexao.commit()
            return True, "Veículo cadastrado com sucesso"

        except Exception as e:
            print (f"Erro ao inserir veículo com placa ({objeto_veiculo.placa}): {e}")
            self.conexao.rollback()
            return False
        
        finally:
            if (cursor):
                cursor.close()


    def remover(self, placa):
        if not self.conexao:
            return False, "Sem conexão com o banco."
            
        try:
            cursor = self.conexao.cursor()
            query = "DELETE FROM tb_veiculos WHERE vei_placa = %s"
            
            cursor.execute(query, (placa,))
            self.conexao.commit()
            
            if cursor.rowcount > 0:
                return True, f"Veículo com placa {placa} removido com sucesso!"
            else:
                return False, "Veículo não encontrado no banco de dados."

        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao remover: {e}"
            
        finally:
            if cursor:
                cursor.close()

    def listar_todos(self):
        if not self.conexao:
            return []
                
        try:
            cursor = self.conexao.cursor()
            query = "SELECT vei_tipo, vei_placa, vei_categoria, vei_taxa_diaria FROM tb_veiculos"
            
            cursor.execute(query) 
            
            linhas = cursor.fetchall()
            veiculos = []
            
            for cada_linha in linhas:
                try:
                    cat_enum = Categoria(cada_linha[2])
                except ValueError:
                    if isinstance(cada_linha[2], str):
                        cat_enum = Categoria[cada_linha[2].upper()]
                    else:
                        raise Exception("Formato de categoria desconhecido no banco de dados.")

                obj = VeiculoFactory.criar_veiculo(
                    tipo_veiculo=cada_linha[0], 
                    placa=cada_linha[1], 
                    categoria=cat_enum, 
                    taxa_diaria=float(cada_linha[3])
                )
                veiculos.append(obj)
            
            return veiculos

        except Exception as e:
            print(f"Erro ao buscar veículos: {e}")
            return []
        
        finally:
            if cursor:
                cursor.close()

    def atualizar(self, objeto_veiculo):
        if not self.conexao:
            return False, "Sem conexão com o Banco de Dados"
        
        try:
            cursor = self.conexao.cursor()
            query = """
                UPDATE tb_veiculos 
                SET vei_tipo = %s, 
                    vei_categoria = %s, 
                    vei_taxa_diaria = %s 
                WHERE vei_placa = %s
            """
            
            valores = (
                objeto_veiculo.__class__.__name__, 
                objeto_veiculo.categoria.value, 
                objeto_veiculo.taxa_diaria, 
                objeto_veiculo.placa
            )
            
            cursor.execute(query, valores)
            self.conexao.commit()
            
            if cursor.rowcount > 0:
                return True, f"Veículo {objeto_veiculo.placa} atualizado com sucesso!"
            else:
                return False, "Veículo não encontrado no banco de dados para atualização."

        except Exception as e:
            print(f"Erro ao atualizar veículo com placa ({objeto_veiculo.placa}): {e}")
            self.conexao.rollback()
            return False, f"Erro ao atualizar: {e}"
        
        finally:
            if cursor:
                cursor.close()

    def buscar_por_placa(self, placa):
        if not self.conexao:
            return None
                
        try:
            cursor = self.conexao.cursor()
            query = "SELECT vei_tipo, vei_placa, vei_categoria, vei_taxa_diaria FROM tb_veiculos WHERE vei_placa = %s"
            
            cursor.execute(query, (placa,))
            
            linha = cursor.fetchone() 
            
            if linha:
                try:
                    cat_enum = Categoria(linha[2])
                except ValueError:
                    if isinstance(linha[2], str):
                        cat_enum = Categoria[linha[2].upper()]
                    else:
                        raise Exception("Formato de categoria desconhecido no banco.")

                veiculo_encontrado = VeiculoFactory.criar_veiculo(
                    tipo_veiculo=linha[0], 
                    placa=linha[1], 
                    categoria=cat_enum, 
                    taxa_diaria=float(linha[3]),
                )
                return veiculo_encontrado
            else:
                return None

        except Exception as e:
            print(f"Erro ao buscar veículo por placa no BD: {e}")
            return None
        
        finally:
            if cursor:
                cursor.close()

