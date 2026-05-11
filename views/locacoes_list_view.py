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

class JanelaListagemLocacoes(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        
        self.title("Locadora de Veículos - Locações")
        self.geometry("850x600")
        
        self.controller = LocacaoController()

        Label(self, text="Locações Cadastradas", font=("Arial", 14, "bold"), pady=10).pack()

        self.tabela = ttk.Treeview(self, columns=("Código", "Placa", "Data Inicio", "Status"), show='headings')
        self.tabela.heading("Código", text="Código")
        self.tabela.heading("Placa", text="Placa")
        self.tabela.heading("Data Inicio", text="Data Inicio")
        self.tabela.heading("Status", text="Status")
        self.tabela.pack()

        self.tabela.bind("<<TreeviewSelect>>", self.verificar_botoes)

        footer = tk.Frame(self, bg="lightgrey", bd=1, relief="raised")
        footer.pack(side="bottom", fill="x")

        tk.Label(footer, text="MENU", bg="lightgrey", fg="black", font=("Arial", 10, "bold")).pack(side="left", padx=10, pady=5)

        tk.Button(footer, text="Sair", command=self.master.destroy).pack(side="right", padx=8, pady=2)

        self.btn_cancelar = tk.Button(footer, text="Cancelar", state="disabled", command=self.cancelar_locacao)
        self.btn_cancelar.pack(side="right", padx=8, pady=2)

        self.btn_devolver = tk.Button(footer, text="Devolver", state="disabled", command=self.devolver_veiculo)
        self.btn_devolver.pack(side="right", padx=8, pady=2)

        self.btn_locar = tk.Button(footer, text="Locar", 
        state="disabled", command=self.locar_veiculooooo)
        self.btn_locar.pack(side="right", padx=8, pady=2)

        tk.Button(footer, text="Ver Detalhes", command=self.ver_detalhes).pack(side="right", padx=8, pady=2)
        
        tk.Button(footer, text="Nova Reserva", command=self.nova_reserva).pack(side="right", padx=8, pady=2)

        self.atualizar_lista_na_tela()


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
        self.verificar_botoes()

    def nova_reserva(self):
        print("Botão Nova Reserva clicado!")

    def ver_detalhes(self):
        selecionado = self.tabela.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma Locação na tabela primeiro.")
            return
        
        valores = self.tabela.item(selecionado[0], "values")
        id_clicada = str(valores[0]).strip()

        locacao = self.controller.buscar_por_codigo(id_clicada)
        if locacao:
            if locacao.status == StatusLocacao.CANCELADO:
                messagebox.showinfo("Informações da Locação", str(locacao.exibir_basico()))
                self.atualizar_lista_na_tela()
            elif locacao.status == StatusLocacao.LOCADO or locacao.status == StatusLocacao.RESERVADO:
                messagebox.showinfo("Informações da Locação", str(locacao.exibir_previsao()))
                self.atualizar_lista_na_tela()
            else:
                messagebox.showinfo("Informações da Locação", str(locacao.exibir_dados()))
                self.atualizar_lista_na_tela()
        else:
            messagebox.showerror("Erro", "Locação não encontrada no Banco de Dados.")

    def locar_veiculooooo(self):
        selecionado = self.tabela.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma Locação na tabela primeiro.")
            return
        
        valores = self.tabela.item(selecionado[0], "values")
        id_clicada = str(valores[0]).strip()

        locacao = self.controller.buscar_por_codigo(id_clicada)

        if not locacao:
            messagebox.showerror("Erro", "Locação não encontrada.")
            return

        if locacao.status == StatusLocacao.RESERVADO:
            sucesso, msg = self.controller.locar_veiculo(id_clicada)
            
            if sucesso:
                messagebox.showinfo("Sucesso", msg)
                self.atualizar_lista_na_tela()
            else:
                messagebox.showerror("Erro", msg)
        else:
            messagebox.showwarning("Aviso", f"Esta locação não pode ser efetivada. Status: {locacao.status.value}")


    def devolver_veiculo(self):
        selecionado = self.tabela.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma Locação na tabela primeiro.")
            return
        
        valores = self.tabela.item(selecionado[0], "values")
        id_clicada = str(valores[0]).strip()

        locacao = self.controller.buscar_por_codigo(id_clicada)

        if not locacao:
            messagebox.showerror("Erro", "Locação não encontrada.")
            return

        if locacao.status == StatusLocacao.LOCADO:
            sucesso, msg = self.controller.devolver_veiculo(id_clicada)
            
            if sucesso:
                messagebox.showinfo("Sucesso", msg)
                self.atualizar_lista_na_tela()
            else:
                messagebox.showerror("Erro", msg)
        else:
            messagebox.showwarning("Aviso", f"Esta ação não pode ser efetivada. Status: {locacao.status.value}")


    def cancelar_locacao(self):
        selecionado = self.tabela.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma Locação na tabela primeiro.")
            return
        
        valores = self.tabela.item(selecionado[0], "values")
        id_clicada = str(valores[0]).strip()

        locacao = self.controller.buscar_por_codigo(id_clicada)

        if not locacao:
            messagebox.showerror("Erro", "Locação não encontrada.")
            return

        if locacao.status == StatusLocacao.RESERVADO:
            sucesso, msg = self.controller.calcelar_reserva(id_clicada)
            
            if sucesso:
                messagebox.showinfo("Sucesso", msg)
                self.atualizar_lista_na_tela()
            else:
                messagebox.showerror("Erro", msg)
        else:
            messagebox.showwarning("Aviso", f"Esta ação não pode ser efetivada. Status: {locacao.status.value}")


    def verificar_botoes(self, event=None):
        selecionado = self.tabela.selection()
        
        if not selecionado:
            self.btn_locar.config(state="disabled")
            self.btn_devolver.config(state="disabled")
            self.btn_cancelar.config(state="disabled")
            return

        valores = self.tabela.item(selecionado[0], "values")
        status = valores[3].lower().strip()

        if status == "reservado":
            self.btn_locar.config(state="normal")
            self.btn_cancelar.config(state="normal")
            self.btn_devolver.config(state="disabled")
            
        elif status == "locado":
            self.btn_locar.config(state="disabled")
            self.btn_cancelar.config(state="disabled")
            self.btn_devolver.config(state="normal")
            
        else:
            self.btn_locar.config(state="disabled")
            self.btn_devolver.config(state="disabled")
            self.btn_cancelar.config(state="disabled")




if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    
    app = JanelaListagemLocacoes(master=root)
    
    app.protocol("WM_DELETE_WINDOW", root.destroy)
    
    root.mainloop()
