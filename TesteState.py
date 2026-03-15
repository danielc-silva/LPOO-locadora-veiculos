from model.VeiculoFactory import VeiculoFactory
from model.Categoria import Categoria

def testar_padrao_state():
    print("\n--- TESTANDO O PADRÃO STATE RESTRITIVO ---")
    
    carro_teste = VeiculoFactory.criar_veiculo("Carro", placa="HJI3K45", taxa_diaria=100.0, categoria=Categoria.ECONOMICO)
    print(f"\nVeículo criado: {carro_teste}")

    print("\nTentando alugar o carro disponível...")
    carro_teste.tentar_alugar()
    
    print("\nTentando alugar o mesmo carro para outro cliente...")
    try:
        carro_teste.tentar_alugar()
    except ValueError as e:
        print(f"Erro capturado: {e}")

    print("\nCliente devolvendo o carro...")
    carro_teste.tentar_devolver()

    print("\nLocadora enviando o carro do pátio para a oficina...")
    carro_teste.reter_na_frota_pra_conserto()

    print("\nCliente tentando alugar o carro que está na oficina...")
    try:
        carro_teste.tentar_alugar()
    except ValueError as e:
        print(f"Erro capturado: {e}")

if __name__ == '__main__':
    testar_padrao_state()