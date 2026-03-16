from model.VeiculoFactory import VeiculoFactory
from model.Categoria import Categoria
from model.Locacao import Locacao
from model.Decoradores import GPSDecorator, SeguroTerceirosDecorator

def testar_padrao_decorator():
    print("\n--- TESTANDO O PADRÃO DECORATOR ---")
    
    # 1. Veículo Base
    carro = VeiculoFactory.criar_veiculo("Carro", placa="DEC1234", taxa_diaria=100.0, categoria=Categoria.ECONOMICO, valor_seguro=20.0)
    
    # 2. Locação Base (Duração de 5 dias)
    print("\nMontando a Locação Base (5 dias)...")
    locacao_base = Locacao(data_inicio="01-03-2026", data_fim=None, veiculo=carro)
    locacao_base.registrar_devolucao_de_veiculo("06-03-2026")
    
    print(f"Valor apenas do pacote base: R$ {locacao_base.valor_locacao}")

    # 3. Adicionando Seguro de Terceiros PRIMEIRO (Para ele ter acesso direto às datas da Base)
    print("\nO cliente adicionou Seguro de Terceiros (+ R$ 15,00/dia)...")
    locacao_com_seguro = SeguroTerceirosDecorator(locacao_base)
    print(f"Valor atualizado (Base + Seguro): R$ {locacao_com_seguro.calcular_valor_locacao()}")

    # 4. Adicionando o GPS POR ÚLTIMO (Como ele tem taxa fixa, não liga para as datas que ficaram escondidas)
    print("\nO cliente também pediu um GPS (+ R$ 35,00 fixo)...")
    locacao_vip_top = GPSDecorator(locacao_com_seguro)
    print(f"Valor do Pacote Completão (Base + Seguro + GPS): R$ {locacao_vip_top.calcular_valor_locacao()}")

if __name__ == '__main__':
    testar_padrao_decorator()