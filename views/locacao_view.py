import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from control.locacao_controller import LocacaoController

class JanelaCadastroLocacao(tk.Toplevel):
    def __init__(self, master=None, locacao_existente=None):
        super().__init__(master)

        self.locacao_existente = locacao_existente
        self.title("Atualizar Locação" if locacao_existente else "Cadastrar Locação")
        self.geometry("380x400")
        self.controller = LocacaoController()

        self.transient(master) 
        self.grab_set()
        self.focus_force()

        texto_titulo = "Atualizar Locação" if locacao_existente else "Cadastrar Locação"
        tk.Label(self, text=texto_titulo, font=("Arial", 14, "bold")).pack(pady=10)

        self.frame_codigo = tk.Frame(self)
        self.frame_codigo.pack(pady=5, fill="x", padx=20)
        tk.Label(self.frame_codigo, text="Código:").pack(side="left")
        self.txt_codigo = tk.Entry(self.frame_codigo)
        self.txt_codigo.pack(side="right", expand=True, fill="x")

        self.frame_placa_manual = tk.Frame(self)
        self.frame_placa_manual.pack(pady=5, fill="x", padx=20)
        tk.Label(self.frame_placa_manual, text="Placa:").pack(side="left")
        self.txt_placa = tk.Entry(self.frame_placa_manual)
        self.txt_placa.pack(side="right", expand=True, fill="x")

        frame_dt_ini = tk.Frame(self)
        frame_dt_ini.pack(pady=5, fill="x", padx=20)
        tk.Label(frame_dt_ini, text="Data início:").pack(side="left")
        self.txt_dt_ini = tk.Entry(frame_dt_ini)
        self.txt_dt_ini.pack(side="right", expand=True, fill="x")

        frame_dt_fim = tk.Frame(self)
        frame_dt_fim.pack(pady=5, fill="x", padx=20)
        tk.Label(frame_dt_fim, text="Data fim:").pack(side="left")
        self.txt_dt_fim = tk.Entry(frame_dt_fim)
        self.txt_dt_fim.pack(side="right", expand=True, fill="x")

        self.frame_cat = tk.Frame(self)
        self.frame_cat.pack(pady=5, fill="x", padx=20)
        tk.Label(self.frame_cat, text="Categoria:").pack(side="left")
        self.cb_categoria = ttk.Combobox(self.frame_cat, values=["Economico", "Executivo", "Luxo"], state="readonly")
        self.cb_categoria.pack(side="right", expand=True, fill="x")
        self.cb_categoria.bind("<<ComboboxSelected>>", self.atualizar_veiculos_livres)

        self.frame_veiculo_selecao = tk.Frame(self)
        tk.Label(self.frame_veiculo_selecao, text="Veículo:").pack(side="left")
        self.cb_placa_busca = ttk.Combobox(self.frame_veiculo_selecao, state="readonly")
        self.cb_placa_busca.pack(side="right", expand=True, fill="x")

        frame_status = tk.Frame(self)
        frame_status.pack(pady=5, fill="x", padx=20)
        tk.Label(frame_status, text="Status:").pack(side="left")
        self.cb_status = ttk.Combobox(frame_status, values=["RESERVADO", "LOCADO", "DEVOLVIDO", "CANCELADO"], state="readonly")
        self.cb_status.current(0)
        self.cb_status.pack(side="right", expand=True, fill="x")

        frame_estrategia_pgt = tk.Frame(self)
        frame_estrategia_pgt.pack(pady=5, fill="x", padx=20)
        tk.Label(frame_estrategia_pgt, text="Estratégia:").pack(side="left")
        self.cb_estrategia_pgt = ttk.Combobox(frame_estrategia_pgt, values=["PADRAO", "VIP"], state="readonly")
        self.cb_estrategia_pgt.current(0)
        self.cb_estrategia_pgt.pack(side="right", expand=True, fill="x")

        self.frame_valor = tk.Frame(self)
        self.frame_valor.pack(pady=5, fill="x", padx=20)
        tk.Label(self.frame_valor, text="Valor (R$):").pack(side="left")
        self.txt_valor = tk.Entry(self.frame_valor)
        self.txt_valor.pack(side="right", expand=True, fill="x")

        btn_cadastrar = tk.Button(self, text=texto_titulo, command=self.solicitar_cadastro)
        btn_cadastrar.pack(pady=20)

        if self.locacao_existente:
            self.txt_codigo.insert(0, str(self.locacao_existente.id))
            self.txt_codigo.config(state="disabled") 
            
            self.frame_placa_manual.pack_forget()

            self.txt_dt_ini.insert(0, self.locacao_existente.data_inicio.strftime("%d/%m/%Y")) 
            self.txt_dt_fim.insert(0, self.locacao_existente.data_fim.strftime("%d/%m/%Y"))
            self.cb_status.set(self.locacao_existente.status.name)
            self.txt_valor.insert(0, f"{self.locacao_existente.valor_locacao:.2f}")
            
            est_nome = "VIP" if "VIP" in str(type(self.locacao_existente.estrategia)) else "PADRAO"
            self.cb_estrategia_pgt.set(est_nome)
            
            cat_atual = getattr(self.locacao_existente.veiculo, "categoria", "Economico")
            self.cb_categoria.set(cat_atual)
            
            nome_veiculo = getattr(self.locacao_existente.veiculo, "modelo", None) or getattr(self.locacao_existente.veiculo, "tipo", "Veículo")
            placa_atual = self.locacao_existente.veiculo.placa
            opcao_atual = f"{nome_veiculo} - {placa_atual}"
            
            self.cb_placa_busca['values'] = [opcao_atual]
            self.cb_placa_busca.set(opcao_atual)
            
            self.frame_veiculo_selecao.pack(pady=5, fill="x", padx=20, after=self.frame_cat)
            
            self.geometry("380x480")
        else:
            self.frame_codigo.pack_forget()
            self.frame_valor.pack_forget()
            self.frame_placa_manual.pack_forget()
            self.cb_status.set("RESERVADO")
            self.cb_status.config(state="disabled")
            self.geometry("380x380")


    def atualizar_veiculos_livres(self, event=None):
        cat = self.cb_categoria.get()
        ini_txt = self.txt_dt_ini.get().strip()
        fim_txt = self.txt_dt_fim.get().strip()

        if not ini_txt or not fim_txt:
            messagebox.showwarning("Aviso", "Preencha as datas primeiro!", parent=self)
            self.cb_categoria.set('')
            return

        try:
            dt_ini = datetime.strptime(ini_txt, "%d/%m/%Y").date()
            dt_fim = datetime.strptime(fim_txt, "%d/%m/%Y").date()
        except Exception:
            messagebox.showerror("Erro", "Formato de data inválido. Use DD/MM/AAAA.", parent=self)
            return

        if dt_fim < dt_ini:
            messagebox.showerror("Erro", "Data fim deve ser posterior à data início.", parent=self)
            return

        livres = self.controller.filtrar_veiculos_disponiveis(cat, ini_txt, fim_txt)

        if not livres:
            messagebox.showinfo("Busca", "Nenhum veículo disponível para estas datas.", parent=self)
            self.frame_veiculo_selecao.pack_forget()
            return

        opcoes = []
        for v in livres:
            nome = getattr(v, "modelo", None) or getattr(v, "nome", None) or getattr(v, "marca", None) or getattr(v, "tipo", None) or "Veículo"
            placa = getattr(v, "placa", "")
            opcoes.append(f"{nome} - {placa}")

        texto_padrao = "Selecione um veículo"
        self.cb_placa_busca['values'] = [texto_padrao] + opcoes
        self.cb_placa_busca.set(texto_padrao)

        self.frame_veiculo_selecao.pack(pady=5, fill="x", padx=20, after=self.frame_cat)
        self.geometry("380x450")


    def solicitar_cadastro(self):
        codigo = self.txt_codigo.get().strip()
        data_inicio = self.txt_dt_ini.get().strip()
        data_fim = self.txt_dt_fim.get().strip()
        status = self.cb_status.get().strip()
        valor = self.txt_valor.get().strip()
        estrategia = self.cb_estrategia_pgt.get().strip()

        selecao_veiculo = self.cb_placa_busca.get()
        
        if "Selecione" in selecao_veiculo or not selecao_veiculo:
            messagebox.showwarning("Aviso", "Por favor, selecione um veículo válido!", parent=self)
            return

        if " - " in selecao_veiculo:
            placa = selecao_veiculo.split(" - ")[1].strip()
        else:
            messagebox.showwarning("Aviso", "Selecione um veículo disponível!", parent=self)
            return

        if self.locacao_existente:
            sucesso, msg = self.controller.editar_locacao(
                codigo=codigo, placa=placa, data_inii=data_inicio,
                data_fim=data_fim, loc_status=status, valor_loc=valor, estrategia_pgt=estrategia
            )
        else: 
            sucesso, msg = self.controller.salvar_locacoes(
                placa_str=placa, locacao_inicio_str=data_inicio, 
                locacao_fim_str=data_fim, status_str=status, estrategia_str=estrategia
            )

        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.destroy()
        else:
            messagebox.showerror("Erro", msg, parent=self)