import tkinter as tk
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from views.veiculo_list_view import JanelaListagemVeiculos
from model.VeiculoFactory import VeiculoFactory
from model.Categoria import Categoria
import views.veiculo_list_view as list_view

if __name__ == "__main__":

    root = tk.Tk()
    root.withdraw()
    
    app = JanelaListagemVeiculos(master=root)
    app.protocol("WM_DELETE_WINDOW", root.destroy)
    
    root.mainloop() 