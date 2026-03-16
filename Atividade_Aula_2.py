from model.Carro import Carro
from model.VeiculoFactory import VeiculoFactory
from model.Categoria import Categoria
from model.Locacao import Locacao
from model.ExcecoesPersonalizadas import TipoVeiculoInvalidoError
from model.LocacaoStrategy import CalculoLocacaoStrategy, CalculoPadraoStrategy, CalculoVIPStrategy

try: 
    print('\nVeículos criados:')
    carro2 = VeiculoFactory.criar_veiculo(
                'Carro', 
                placa='BRA2E19', 
                taxa_diaria=180.50,
                categoria=Categoria.ECONOMICO
            )
    print(carro2)

    Motorhome1 = VeiculoFactory.criar_veiculo(
                'Motorhome', 
                placa='BRA2E20', 
                taxa_diaria=300.90,
                categoria=Categoria.EXECUTIVO,
                valor_seguro=90.00
            )
    print(Motorhome1)
    print('\n')

    # Teste de múltiplos dias (8 dias)
    locacao1 = Locacao("12-2-2026", data_fim=None, veiculo=Motorhome1)
    locacao1.registrar_devolucao_de_veiculo("20-2-2026")
    print(locacao1)

    # Teste de devolução com dias negativos (Devolução ANTES do início)
    locacao2 = Locacao("15-2-2026", data_fim=None, veiculo=carro2)
    locacao2.registrar_devolucao_de_veiculo("10-2-2026")
    print(locacao2)

    # CRIAMOS UM CARRO NOVO AQUI, POIS O CARRO 2 CONTINUA ALUGADO (A DEVOLUÇÃO ACIMA FALHOU)
    carro3 = VeiculoFactory.criar_veiculo(
                'Carro', 
                placa='BRA2E21', 
                taxa_diaria=180.50,
                categoria=Categoria.ECONOMICO
            )

    # Teste de devolução no mesmo dia (0 dias) - Usando o carro3 que está Disponível
    locacao3 = Locacao("12-2-2026", data_fim=None, veiculo=carro3)
    locacao3.registrar_devolucao_de_veiculo("12-2-2026")
    print(locacao3)

    # Tentando criar um Veículo inválido
    Onibus = VeiculoFactory.criar_veiculo(
                'Onibus', 
                placa='BRA2E20', 
                taxa_diaria=1000.0,
                categoria=Categoria.EXECUTIVO,
                valor_seguro=200.00
            )

except TipoVeiculoInvalidoError as erro:
    print(f'{erro}')