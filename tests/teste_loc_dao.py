import sys
import os
import traceback
from datetime import date

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dao.locacao_dao import LocacaoDAO
from model.VeiculoFactory import VeiculoFactory
from model.Categoria import Categoria 
from model.Locacao import Locacao
from model.StatusLocacao import StatusLocacao

def testar_dao():
    print("Iniciando testes detalhados do LocacaoDAO com Factory...\n")
    
    try:
        dao = LocacaoDAO()
    except Exception as e:
        print("ERRO CRITICO: Falha ao conectar no banco de dados!")
        print(f"Detalhe: {e}")
        return

    placa_teste = "DES5647" 
    
    try:
        carro_teste = VeiculoFactory.criar_veiculo(
            tipo_veiculo='Carro', 
            placa=placa_teste, 
            categoria=Categoria.ECONOMICO, 
            taxa_diaria=100.0
        )
    except Exception as e:
        print(f"ERRO AO CRIAR VEICULO PELA FABRICA: {e}")
        return

    nova_locacao = Locacao(
        veiculo=carro_teste,
        data_inicio=date(2026, 5, 7),
        data_fim=date(2026, 5, 15),
        status=StatusLocacao.RESERVADO
    )
    
    print(f"--- TESTE 1: SALVANDO LOCACAO (Placa: {placa_teste}) ---")
    try:
        sucesso, resultado = dao.salvar(nova_locacao)
        if sucesso:
            print(f"SUCESSO: {resultado}")
        else:
            print(f"FALHA NO BANCO DE DADOS: {resultado}")
    except Exception as e:
        print(f"ERRO DE CODIGO NO PYTHON (SALVAR): {e}")
        traceback.print_exc()

    print("\n--- TESTE 2: LISTANDO LOCACOES ---")
    try:
        lista_locacoes = dao.listar_todos()
        if not lista_locacoes:
            print("AVISO: Lista vazia (nenhuma locacao encontrada).")
        else:
            print(f"SUCESSO: {len(lista_locacoes)} locacoes encontradas!")
            for loc in lista_locacoes:
                placa = loc.veiculo.placa if hasattr(loc.veiculo, 'placa') else loc.veiculo
                print(f"ID: {getattr(loc, 'id', 'N/A')} | Placa: {placa} | Status: {loc.status.name}")
    except Exception as e:
        print(f"ERRO DE CODIGO NO PYTHON (LISTAR): {e}")
        traceback.print_exc()

if __name__ == "__main__":
    testar_dao()