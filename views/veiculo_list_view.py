import tkinter as tk
from tkinter import ttk, Label, Button, messagebox
import sys
import os

caminho_projeto = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(caminho_projeto)

from control.veiculo_controller import VeiculoController 
from views.veiculo_view import JanelaCadastroVeiculo 

class JanelaListagemVeiculos(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        
        self.title("Locadora de Veículos")
        self.geometry("1050x600")
        
        self.controller = VeiculoController()

        Label(self, text="Veículos Cadastrados", font=("Arial", 14, "bold"), pady=10).pack()

        self.tabela = ttk.Treeview(self, columns=("Nome", "Placa", "Categoria", "Taxa Diária", "Seguro"), show='headings')
        self.tabela.heading("Nome", text="Nome")
        self.tabela.heading("Placa", text="Placa")
        self.tabela.heading("Categoria", text="Categoria")
        self.tabela.heading("Taxa Diária", text="Taxa Diária")
        self.tabela.heading("Seguro", text="Seguro")
        self.tabela.pack()

        footer = tk.Frame(self, bg="lightgrey", bd=1, relief="raised")
        footer.pack(side="bottom", fill="x")

        tk.Label(footer, text="MENU", bg="lightgrey", fg="black", font=("Arial", 10, "bold")).pack(side="left", padx=10, pady=5)

        tk.Button(footer, text="Sair", command=self.master.destroy).pack(side="right", padx=8, pady=2)
        tk.Button(footer, text="Remover", command=self.remover_veiculo).pack(side="right", padx=8, pady=2)
        tk.Button(footer, text="Atualizar", command=self.abrir_tela_edicao).pack(side="right", padx=8, pady=2)
        tk.Button(footer, text="Ver Informações", command=self.ver_informacoes).pack(side="right", padx=8, pady=2)
        tk.Button(footer, text="Novo", command=self.abrir_tela_cadastro).pack(side="right", padx=8, pady=2)

        self.atualizar_lista_na_tela()

    def atualizar_lista_na_tela(self):
        for item in self.tabela.get_children():
            self.tabela.delete(item)
            
        veiculos = self.controller.listar_veiculos()
        
        if veiculos: 
            for veiculo in veiculos:
                tipo = veiculo.__class__.__name__
                self.tabela.insert("", tk.END, values=(
                    tipo, 
                    veiculo.placa, 
                    veiculo.categoria.name.capitalize(), 
                    f"R$ {veiculo.taxa_diaria:.2f}",  
                    f"R$ {veiculo.valor_seguro:.2f}"
                ))

    def abrir_tela_cadastro(self):
        janela_cadastro = JanelaCadastroVeiculo(self)
        self.wait_window(janela_cadastro)
        self.atualizar_lista_na_tela()

    def abrir_tela_edicao(self):
        selecionado = self.tabela.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um veículo na tabela primeiro para editar.")
            return
        
        valores = self.tabela.item(selecionado[0], "values")
        placa_clicada = str(valores[1]).strip()
        
        veiculo_para_editar = self.controller.buscar_por_placa(placa_clicada)
        
        if veiculo_para_editar:
            janela_edicao = JanelaCadastroVeiculo(self, veiculo_existente=veiculo_para_editar)
            self.wait_window(janela_edicao)
            self.atualizar_lista_na_tela()
        else:
            messagebox.showerror("Erro", "Não foi possível carregar os dados do veículo.")

    def ver_informacoes(self):
        selecionado = self.tabela.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um veículo na tabela primeiro.")
            return
        
        valores = self.tabela.item(selecionado[0], "values")
        placa_clicada = str(valores[1]).strip() 
        
        veiculo = self.controller.buscar_por_placa(placa_clicada)
        if veiculo:
            messagebox.showinfo("Informações do Veículo", str(veiculo.exibir_dados()))
        else:
            messagebox.showerror("Erro", "Veículo não encontrado no Banco de Dados.")

    def remover_veiculo(self):
        selecionado = self.tabela.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um veículo na tabela primeiro para remover.")
            return
        
        valores = self.tabela.item(selecionado[0], "values")
        placa_clicada = str(valores[1]).strip()
        
        sucesso, mensagem = self.controller.remover_veiculo(placa_clicada)
        if sucesso:
            self.atualizar_lista_na_tela() 
            messagebox.showinfo("Sucesso", mensagem)
        else:
            messagebox.showwarning("Aviso", mensagem)