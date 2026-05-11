import tkinter as tk
from tkinter import Menu
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from views.veiculo_list_view import JanelaListagemVeiculos
from views.locacoes_list_adm import JanelaListagemLocacoesAdm
from views.locacoes_list_view import JanelaListagemLocacoes

class JanelaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Locadora de Veículos")
        self.geometry("600x200")
        
        self.barra_menus = Menu(self)
        self.config(menu=self.barra_menus)

        self.menu_cadastro = Menu(self.barra_menus, tearoff=0)
        self.barra_menus.add_cascade(label="Cadastro", menu=self.menu_cadastro)
        
        self.menu_cadastro.add_command(label="Veículo", command=self.abrir_listagem_veiculos)
        self.menu_cadastro.add_command(label="Locações (Admin)", command=self.abrir_listagem_locacoes_adm)
        
        self.menu_cadastro.add_separator()
        self.menu_cadastro.add_command(label="Sair", command=self.quit)

        self.menu_acao = Menu(self.barra_menus, tearoff=0)
        self.barra_menus.add_cascade(label="Ação", menu=self.menu_acao)
        
        self.menu_acao.add_command(label="Locar Veículo", command=self.abrir_operacional_usuario)

        tk.Label(self, text="Bem-vindo ao Sistema da Locadora", font=("Arial", 20, "bold")).pack(expand=True)
        tk.Label(self, text="Utilize o menu acima.", font=("Arial", 10)).pack(expand=True)


    def abrir_listagem_veiculos(self):
        self.withdraw()
        janela = JanelaListagemVeiculos(self)
        self.wait_window(janela)
        self.deiconify()

    def abrir_listagem_locacoes_adm(self):
        self.withdraw()
        janela = JanelaListagemLocacoesAdm(self)
        self.wait_window(janela)
        self.deiconify()

    def abrir_operacional_usuario(self):
        self.withdraw()
        janela = JanelaListagemLocacoes(self)
        self.wait_window(janela)
        self.deiconify()