import tkinter as tk
from tkinter import ttk, Label, Button, messagebox
import sys
import os

caminho_projeto = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(caminho_projeto)

from control.locacao_controller import LocacaoController
from dao.veiculo_dao import VeiculoDAO
from dao.locacao_dao import LocacaoDAO
from model.StatusLocacao import StatusLocacao

class JanelaListagemLocacoesAdm(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        
        self.title("Locadora de Veículos - Painel de Adm")
        self.geometry("850x600")
        
        self.controller = LocacaoController()

        Label(self, text="Locações Cadastradas", font=("Arial", 14, "bold"), pady=10).pack()

        self.tabela = ttk.Treeview(self, columns=("Código", "Placa", "Data Inicio", "Status"), show='headings')
        self.tabela.heading("Código", text="Código")
        self.tabela.heading("Placa", text="Placa")
        self.tabela.heading("Data Inicio", text="Data Inicio")
        self.tabela.heading("Status", text="Status")
        self.tabela.pack()

        footer = tk.Frame(self, bg="lightgrey", bd=1, relief="raised")
        footer.pack(side="bottom", fill="x")

        tk.Label(footer, text="MENU ADMINISTRADOR", bg="lightgrey", fg="black", font=("Arial", 10, "bold")).pack(side="left", padx=10, pady=5)     

        tk.Button(footer, text="Sair", command=self.master.destroy).pack(side="right", padx=8, pady=2)

        tk.Button(footer, text="Remover", command=self.remover_locacao).pack(side="right", padx=8, pady=2)

        tk.Button(footer, text="Ver Detalhes", command=self.ver_detalhes).pack(side="right", padx=8, pady=2)

        tk.Button(footer, text="Editar", command=self.editar_locacao).pack(side="right", padx=8, pady=2)

        tk.Button(footer, text="Nova Reserva", command=self.nova_reserva).pack(side="right", padx=8, pady=2)

        self.atualizar_lista_na_tela()


    def remover_locacao (self):
        selecionado = self.tabela.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma locação na tabela para remover.")
            return
        
        valores = self.tabela.item(selecionado[0], "values")
        locacao_clicada = str(valores[0]).strip()

        sucesso, mensagem = self.controller.remover_locacao(locacao_clicada)
        if sucesso:
            self.atualizar_lista_na_tela() 
            messagebox.showinfo("Sucesso", mensagem)
        else:
            messagebox.showwarning("Aviso", mensagem)


    def editar_locacao (self):
        pass


    def ver_detalhes(self):
        selecionado = self.tabela.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma Locação na tabela primeiro.")
            return
        
        valores = self.tabela.item(selecionado[0], "values")
        id_clicada = str(valores[0]).strip()

        locacao = self.controller.buscar_por_codigo(id_clicada)
        if locacao:
                messagebox.showinfo("Informações da Locação", str(locacao.exibir_dados()))
                self.atualizar_lista_na_tela()
        else:
            messagebox.showerror("Erro", "Locação não encontrada no Banco de Dados.")


    def atualizar_lista_na_tela(self):
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        locacoes = self.controller.listar_locacoes()

        if locacoes:
            for locacao in locacoes:
                status_loc = locacao.status.value
                self.tabela.insert("", tk.END, values= (
                    locacao.id,
                    locacao.veiculo.placa,
                    locacao.data_inicio,
                    status_loc.upper()
                ))

    def nova_reserva(self):
        print("Botão Nova Reserva clicado!")


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    
    app = JanelaListagemLocacoesAdm(master=root)
    
    app.protocol("WM_DELETE_WINDOW", root.destroy)
    
    root.mainloop()









