from model.VeiculoFactory import VeiculoFactory
from model.Categoria import Categoria
from model.ExcecoesPersonalizadas import PlacaInvalidaError

def testar_factory():
    print("="*40)
    print("INICIANDO TESTES DA VEICULO FACTORY")
    print("="*40)




    print("\n[Teste 1] Criando um Carro válido...")
    try:
        carro = VeiculoFactory.criar_veiculo(
            'Carro', 
            placa='BRA2E19', 
            taxa_diaria=180.50,
            categoria=Categoria.EXECUTIVO
        )
        # O Setter limpou a placa? A taxa entrou certa?
        if carro.placa == 'BRA2E19' and carro.taxa_diaria == 180.50:
            print("SUCESSO: Carro criado e validado corretamente!")
            print(f" ---> Retorno: {carro}")
        else:
            print("FALHA: O carro foi criado, mas os dados estão errados.")
    except Exception as e:
        print(f"FALHA INESPERADA: {e}")

 


    print("\n[Teste 2] Criando um Motorhome com placa errada...")
    try:
        motorhome = VeiculoFactory.criar_veiculo(
            'Motorhome', 
            placa='1234567', # Placa só com números para dar erro 
            taxa_diaria=300.0
        )
        print("FALHA: A placa errada foi aceita, o sistema falhou em barrar!")
    except PlacaInvalidaError as e:
        print(f"SUCESSO: O sistema bloqueou a placa corretamente.")
        print(f" ---> Motivo bloqueado: {e}")
    except Exception as e:
        print(f"FALHA INESPERADA: Deu erro, mas não foi o de Placa. Erro: {e}")


    print("\n[Teste 3] Solicitando veículo desconhecido...")
    try:
        caminhao = VeiculoFactory.criar_veiculo('Caminhao', placa='ABC1234')
        print("FALHA: A Factory criou um Caminhão que não existe no código!")
    except ValueError as e:
        print("SUCESSO: A Factory impediu a criação de um tipo desconhecido.")
        print(f" ---> Motivo bloqueado: {e}")

    print("\n" + "="*40)
    print("TESTES FINALIZADOS")
    print("="*40)


if __name__ == '__main__':
    testar_factory()