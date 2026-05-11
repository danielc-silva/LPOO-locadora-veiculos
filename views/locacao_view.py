import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import messagebox, ttk
from control.locacao_controller import LocacaoController
from control.veiculo_controller import VeiculoController

class JanelaCadastroLocacao(tk.Toplevel):
    def __init__(self, master=None, locacao_existente=None):
        super().__init__(master)

        self.locacao_existente = locacao_existente
        self.title("Atualizar Locação" if locacao_existente else "Cadastrar Locação")

        self.geometry("350x325")
        self.controller = LocacaoController()

        self.transient(master) 
        self.grab_set()
        self.focus_force()

        texto_titulo = "Atualizar Locação" if locacao_existente else "Cadastrar Locação"
        tk.Label(self, text=texto_titulo, font=("Arial", 14, "bold")).pack(pady=10)

        frame_codigo = tk.Frame(self)
        frame_codigo.pack(pady=5, fill="x", padx=20)
        tk.Label(frame_codigo, text="Código:").pack(side="left")
        self.txt_codigo = tk.Entry(frame_codigo)
        self.txt_codigo.pack(side="right", expand=True, fill="x")

        frame_placa = tk.Frame(self)
        frame_placa.pack(pady=5, fill="x", padx=20)
        tk.Label(frame_placa, text="Placa:").pack(side="left")
        self.txt_placa = tk.Entry(frame_placa)
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


        frame_status = tk.Frame(self)
        frame_status.pack(pady=5, fill="x", padx=20)
        tk.Label(frame_status, text="Status:").pack(side="left")
        self.cb_status = ttk.Combobox(frame_status, values=["RESERVADO", "LOCADO", "DEVOLVIDO", "CANCELADO"], state="readonly")
        self.cb_status.current(0)
        self.cb_status.pack(side="right", expand=True, fill="x")


        frame_estrategia_pgt = tk.Frame(self)
        frame_estrategia_pgt.pack(pady=5, fill="x", padx=20)
        tk.Label(frame_estrategia_pgt, text="Estratégia de Pagamento:").pack(side="left")
        self.cb_estrategia_pgt = ttk.Combobox(frame_estrategia_pgt, values=[ "PADRAO", "VIP"], state="readonly")
        self.cb_estrategia_pgt.current(0)
        self.cb_estrategia_pgt.pack(side="right", expand=True, fill="x")

        frame_valor = tk.Frame(self)
        frame_valor.pack(pady=5, fill="x", padx=20)
        tk.Label(frame_valor, text="Valor (R$):").pack(side="left")
        self.txt_valor = tk.Entry(frame_valor)
        self.txt_valor.pack(side="right", expand=True, fill="x")

        texto_botao = "Atualizar Locação" if locacao_existente else "Salvar Locação"
        btn_cadastrar = tk.Button(self, text=texto_botao, command=self.solicitar_cadastro)
        btn_cadastrar.pack(pady=20)

    def solicitar_cadastro(self):
        codigo = self.txt_codigo.get().strip()
        placa = self.txt_placa.get().strip().upper()
        data_inicio = self.txt_dt_ini.get().strip()
        data_fim = self.txt_dt_fim.get().strip()
        status = self.cb_status.get().strip()
        valor = self.txt_valor.get().strip()
        estrategia = self.cb_estrategia_pgt.get().strip()

        if self.locacao_existente:
            sucesso, msg = self.controller.editar_locacao(codigo= codigo, placa= placa, data_ini= data_inicio, data_fim= data_fim, loc_status= status, valor_loc= valor, estrategia_pgt= estrategia)
        else: 
            sucesso, msg = self.controller.salvar_locacoes( placa_str= placa, locacao_inicio_str= data_inicio, locacao_fim_str= data_fim, status_str= status, estrategia_str= estrategia)

        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.destroy()
        else:
            messagebox.showerror("Erro", msg, parent=self)











if __name__ == "__main__":
    root = tk.Tk()
    # Em vez de withdraw(), vamos apenas definir o título para o root
    # ou usar o próprio app como janela principal se for apenas para teste.
    
    app = JanelaCadastroLocacao(master=root)
    
    # Faz com que, ao fechar a janela de cadastro, o programa todo encerre
    app.protocol("WM_DELETE_WINDOW", root.destroy)
    
    root.mainloop()