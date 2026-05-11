import tkinter as tk
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from views.veiculo_list_view import JanelaListagemVeiculos
from model.VeiculoFactory import VeiculoFactory
from model.Categoria import Categoria
from views.janela_principal import JanelaPrincipal 


if __name__ == "__main__":
    app = JanelaPrincipal()
    app.mainloop()