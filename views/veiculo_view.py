import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import messagebox, ttk
from control.veiculo_controller import VeiculoController

class JanelaCadastroVeiculo(tk.Toplevel):
    def __init__(self, master=None, veiculo_existente=None):
        super().__init__(master)
        
        self.veiculo_existente = veiculo_existente
        self.title("Atualizar Veículo" if veiculo_existente else "Cadastro de Novo Veículo")
        
        self.geometry("350x300")
        self.controller = VeiculoController()
        
        self.transient(master) 
        self.grab_set()        
        self.focus_force()     
        
        texto_titulo = "Atualizar Veículo" if veiculo_existente else "Cadastrar Veículo"
        tk.Label(self, text=texto_titulo, font=("Arial", 14, "bold")).pack(pady=10)

        
        frame_placa = tk.Frame(self)
        frame_placa.pack(pady=5, fill="x", padx=20)
        tk.Label(frame_placa, text="Placa:").pack(side="left")
        self.txt_placa = tk.Entry(frame_placa)
        self.txt_placa.pack(side="right", expand=True, fill="x")

        frame_tipo = tk.Frame(self)
        frame_tipo.pack(pady=5, fill="x", padx=20)
        tk.Label(frame_tipo, text="Tipo:").pack(side="left")
        self.cb_tipo = ttk.Combobox(frame_tipo, values=["Carro", "Motorhome"], state="readonly")
        self.cb_tipo.set("Carro")
        self.cb_tipo.pack(side="right", expand=True, fill="x")

        frame_cat = tk.Frame(self)
        frame_cat.pack(pady=5, fill="x", padx=20)
        tk.Label(frame_cat, text="Categoria:").pack(side="left")
        self.cb_categoria = ttk.Combobox(frame_cat, values=["ECONOMICO", "EXECUTIVO", "LUXO"], state="readonly")
        self.cb_categoria.current(0)
        self.cb_categoria.pack(side="right", expand=True, fill="x")

        frame_taxa = tk.Frame(self)
        frame_taxa.pack(pady=5, fill="x", padx=20)
        tk.Label(frame_taxa, text="Taxa Diária (R$):").pack(side="left")
        self.txt_taxa = tk.Entry(frame_taxa)
        self.txt_taxa.pack(side="right", expand=True, fill="x")

        texto_botao = "Atualizar Veículo" if veiculo_existente else "Salvar Veículo"
        btn_cadastrar = tk.Button(self, text=texto_botao, command=self.solicitar_cadastro)
        btn_cadastrar.pack(pady=20)
        
        if self.veiculo_existente:
            self.txt_placa.insert(0, self.veiculo_existente.placa)
            self.txt_placa.config(state="disabled") 
            self.cb_tipo.set(self.veiculo_existente.__class__.__name__) 
            self.cb_categoria.set(self.veiculo_existente.categoria.name.upper())
            self.txt_taxa.insert(0, f"{self.veiculo_existente.taxa_diaria}")

    def solicitar_cadastro(self):
        placa = self.txt_placa.get().strip().upper()
        tipo = self.cb_tipo.get().strip()
        categoria = self.cb_categoria.get().strip()
        taxa_str = self.txt_taxa.get().strip()

        if self.veiculo_existente:
            sucesso, msg = self.controller.atualizar_veiculo(placa_str=placa, tipo_str=tipo, categoria_str=categoria, taxa_str=taxa_str)
        else:
            sucesso, msg = self.controller.salvar_veiculo(placa_str=placa, tipo_str=tipo, categoria_str=categoria, taxa_str=taxa_str)
        
        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.destroy()
        else:
            messagebox.showerror("Erro", msg, parent=self)