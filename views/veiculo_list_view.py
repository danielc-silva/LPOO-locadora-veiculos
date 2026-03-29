import tkinter as tk
from tkinter import ttk 
from tkinter import Label, Entry, Button, messagebox

import sys
import os
caminho_projeto = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(caminho_projeto)

from model.VeiculoFactory import VeiculoFactory

veiculos_em_memoria = [] # armazena os veículos criados

def atualizar_lista_na_tela():
    for item in tabela.get_children():
        tabela.delete(item)
        
    for veiculo in veiculos_em_memoria:
        tipo = veiculo.__class__.__name__
        
        tabela.insert("", tk.END, values=(
            tipo, 
            veiculo.placa, 
            veiculo.categoria.name.capitalize(), 
            f"R$ {veiculo.taxa_diaria:.2f}",  
            f"R$ {veiculo.valor_seguro:.2f}"
        ))


def cadastrar_veiculo():
    cadastrar = tk.Toplevel(janela)
    cadastrar.title("Formulário de Cadastro")
    cadastrar.geometry("300x300")

    cadastrar.transient(janela)
    cadastrar.grab_set()
    cadastrar.focus_force()

    lbl_titulo = Label(cadastrar, text="Cadastrar Veículo", font=("Arial", 14, "bold"), pady=10).pack()

    def salvar_veiculo():
        try:
            novo_veiculo = VeiculoFactory.criar_veiculo(
                tipo_veiculo=str(combo_tipo.get()),
                placa=str(txt_placa.get()).replace(" ", ""), 
                categoria=str(combo_categoria.get()),
                taxa_diaria=float(txt_taxa_diaria_digitada.get())
            )
            
            veiculos_em_memoria.append(novo_veiculo)
            atualizar_lista_na_tela()
            
            messagebox.showinfo("Sucesso", "Veículo cadastrado!")
            cadastrar.destroy()
            
        except Exception as erro:

            messagebox.showwarning("Atenção", str(erro))

    lbl_placa = Label(cadastrar, text="Placa:").pack()
    txt_placa = Entry(cadastrar)
    txt_placa.pack(pady=5)

    lbl_taxa_diaria_digitada = Label(cadastrar, text="Taxa diária:").pack()
    txt_taxa_diaria_digitada = Entry(cadastrar)
    txt_taxa_diaria_digitada.pack(pady=5)

    combo_tipo = ttk.Combobox(cadastrar, values=["Carro", "Motorhome"], state="readonly")
    combo_tipo.set("Selecione o Tipo")
    combo_tipo.pack(pady=5)

    combo_categoria = ttk.Combobox(cadastrar, values=["Economico", "Executivo"], state="readonly")
    combo_categoria.set("Selecione a Categoria")
    combo_categoria.pack(pady=5)
    
    btn_calcular = Button(cadastrar, text="Salvar", command=salvar_veiculo).pack()
    

def ver_informacoes():
    selecionado = tabela.selection()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione um veículo na tabela primeiro.")
        return
    
    valores = tabela.item(selecionado[0], "values")
    
    placa_clicada = str(valores[1]).strip() 
    
    for veiculo in veiculos_em_memoria:
        if str(veiculo.placa).strip() == placa_clicada:
            messagebox.showinfo("Informações do Veículo", str(veiculo.exibir_dados()))
            break

    
def remover_veiculo():
    global veiculos_em_memoria
    
    selecionado = tabela.selection()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione um veículo na tabela primeiro para remover.")
        return
    
    valores = tabela.item(selecionado[0], "values")
    
    placa_clicada = str(valores[1]).strip()
    
    veiculos_em_memoria = [v for v in veiculos_em_memoria if str(v.placa).strip() != placa_clicada]
    
    atualizar_lista_na_tela()
    messagebox.showinfo("Sucesso", f"O veículo com placa {placa_clicada} foi removido com sucesso!")

#####################################################################################################################################################
# 1. Criar a janela
janela = tk.Tk()

# 2. Configuração da janela
janela.title("Locadora de Veículos")
janela.geometry("1050x600")

lbl_titulo = Label(janela, text="Veículos Cadastrados", font=("Arial", 14, "bold"), pady=10).pack()

tabela = ttk.Treeview(janela, columns=("Nome", "Placa", "Categoria", "Taxa Diária", "Seguro"), show='headings')
tabela.heading("Nome", text="Nome")
tabela.heading("Placa", text="Placa")
tabela.heading("Categoria", text="Categoria")
tabela.heading("Taxa Diária", text="Taxa Diária")
tabela.heading("Seguro", text="Seguro")

tabela.pack()

# tree.insert("", tk.END, values=("2", "Item B"))

footer = tk.Frame(janela, bg="lightgrey", bd=1, relief="raised")
footer.pack(side="bottom", fill="x")

# 2. Adicionar itens (labels/buttons) ao rodapé
label_menu = tk.Label(footer, text="MENU", bg="lightgrey", fg="black", font=("Arial", 10, "bold"))
label_menu.pack(side="left", padx=10, pady=5)

button_sair = tk.Button(footer, text="Sair", command=janela.quit)
button_sair.pack(side="right", padx=8, pady=2)

btn_remover = tk.Button(footer, text="Remover", command= remover_veiculo)
btn_remover.pack (side = "right", padx = 8, pady = 2)

btn_verInfo = tk.Button(footer, text="Ver Informações", command= ver_informacoes)
btn_verInfo.pack (side = "right", padx = 8, pady = 2)

btn_novo = tk.Button(footer, text="Novo", command= cadastrar_veiculo)
btn_novo.pack (side = "right", padx = 8, pady = 2)


janela.mainloop()
