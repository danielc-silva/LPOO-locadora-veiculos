import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.Veiculo import *
from dao.veiculo_dao import VeiculoDAO
from model.VeiculoFactory import VeiculoFactory

dao = VeiculoDAO()

novo_carro = VeiculoFactory.criar_veiculo(
    "Carro", 
    placa="ABC1D34", 
    categoria=Categoria.ECONOMICO, 
    taxa_diaria=150
)

dao.salvar(novo_carro)

lista_veiculos = dao.listar_todos()

print(f"Total de Veículos cadastrados: {len(lista_veiculos)}\n")
for obj in lista_veiculos:
    print(obj.exibir_dados())
