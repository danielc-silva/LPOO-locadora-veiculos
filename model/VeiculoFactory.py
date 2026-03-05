from .Carro import Carro
from .Motorhome import Motorhome

from .Carro import Carro
from .Motorhome import Motorhome
from .Categoria import Categoria

class VeiculoFactory():
    @staticmethod
    def criar_veiculo(tipo_veiculo: str, **args):
        if tipo_veiculo == 'Carro':
            # Veja que aqui NÃO passamos o valor_seguro
            return Carro(
                placa=args.get('placa', None),
                categoria=args.get('categoria', Categoria.ECONOMICO),
                taxa_diaria=args.get('taxa_diaria', 0.0),
                valor_seguro=args.get('valor_seguro', 50.00)
            )
            
        elif tipo_veiculo == 'Motorhome':
            # Aqui também NÃO passamos o valor_seguro
            return Motorhome(
                placa=args.get('placa', None),
                categoria=args.get('categoria', Categoria.ECONOMICO),
                taxa_diaria=args.get('taxa_diaria', 0.0),
                valor_seguro=args.get('valor_seguro', 120.00)
            ) 
            
        else:
            raise ValueError(f'Tipo de veículo desconhecido: {tipo_veiculo}')
