import tkinter as tk
from tkinter import ttk, Label, Button, messagebox
import sys
import os

caminho_projeto = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(caminho_projeto)

class JanelaListagemLocacoes(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        
        self.title("Locadora de Veículos - Locações")
        self.geometry("850x600")
        
        # self.controller = LocacaoController() # precisamos criar o controlerr para a loc
        Label(self, text="Locações Cadastradas", font=("Arial", 14, "bold"), pady=10).pack()

        self.tabela = ttk.Treeview(self, columns=("Código", "Placa", "Data Inicio", "Status"), show='headings')
        self.tabela.heading("Código", text="Código")
        self.tabela.heading("Placa", text="Placa")
        self.tabela.heading("Data Inicio", text="Data Inicio")
        self.tabela.heading("Status", text="Status")
        self.tabela.pack()

        footer = tk.Frame(self, bg="lightgrey", bd=1, relief="raised")
        footer.pack(side="bottom", fill="x")

        tk.Label(footer, text="MENU", bg="lightgrey", fg="black", font=("Arial", 10, "bold")).pack(side="left", padx=10, pady=5)

        tk.Button(footer, text="Sair", command=self.master.destroy).pack(side="right", padx=8, pady=2)
        tk.Button(footer, text="Cancelar", command=self.cancelar_locacao).pack(side="right", padx=8, pady=2)
        tk.Button(footer, text="Devolver", command=self.devolver_veiculo).pack(side="right", padx=8, pady=2)
        tk.Button(footer, text="Locar", command=self.locar_veiculo).pack(side="right", padx=8, pady=2)
        tk.Button(footer, text="Ver Detalhes", command=self.ver_detalhes).pack(side="right", padx=8, pady=2)
        tk.Button(footer, text="Nova Reserva", command=self.nova_reserva).pack(side="right", padx=8, pady=2)

        self.atualizar_lista_na_tela()


    def atualizar_lista_na_tela(self):
        print("Atualizando a lista na tela.")

    def nova_reserva(self):
        print("Botão Nova Reserva clicado!")

    def ver_detalhes(self):
        print("Botão Ver Detalhes clicado!")

    def locar_veiculo(self):
        print("Botão  Locar clicado!")

    def devolver_veiculo(self):
        print("Botão Devolver clicado!")

    def cancelar_locacao(self):
        print("Botão Cancelar clicado!")


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    
    app = JanelaListagemLocacoes(master=root)
    
    app.protocol("WM_DELETE_WINDOW", root.destroy)
    
    root.mainloop()
