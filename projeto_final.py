import sqlite3 # banco de dados
import tkinter as tk # lib de interface gráfica
from tkinter import messagebox, ttk # caixa de msg / tkinter


def conectar():
    return sqlite3.connect('teste.db')

# CREATE READ UPDATE DELETE

# banco de dados
def criar_tabela():
    conn = conectar()
    c = conn.cursor() # digitar sql num arquivo python
    c.execute('''
               CREATE TABLE IF NOT EXISTS pecas(
             
              lote INTEGER NOT NULL,
              operacao TEXT NOT NULL,
              data TEXT NOT NULL,
              situacao TEXT NOT NULL
             
              )''')
    conn.commit()
    conn.close()          



# CREATE CRUD

def inserir_peca():
    lote   =  entry_lote.get().strip()
    operacao  =  entry_operacao.get().strip()
    data =  entry_data.get().strip()
    situacao = entry_situacao.get().strip()
   
    if lote and operacao and data:
    #    try:
            conn  =  conectar()
            c = conn.cursor()
            c.execute('INSERT INTO pecas (lote, operacao, data, situacao) VALUES (?,?,?,?)', (lote, operacao, data, situacao))
            conn.commit()
            conn.close()
            messagebox.showinfo('Dados','DADOS INSERIDOS COM SUCESSO!')
            mostra_peca()
            entry_lote.delete(0, tk.END)
            entry_operacao.delete(0, tk.END)
            entry_data.delete(0, tk.END)
    #    except sqlite3.IntegrityError:
    #         messagebox.showerror('Erro', 'O DADO JA EXISTE')

    else:
        messagebox.showwarning('Dado', 'INSIRA TODOS OS DADOS')


def mostra_peca():
    for row in tree.get_children():
        tree.delete(row)
    conn  =  conectar()
    c = conn.cursor()        
    c.execute('SELECT * FROM pecas')
    pecas =  c.fetchall()
    for peca in pecas:
        tree.insert('', 'end', values=peca)
    conn.close()    


# ATUALIZAR
def editar():
    selecao = tree.selection()
    numero_lote  =  tree.item(selecao)['values'][0]
    if selecao:
       
        novo_operacao  =  entry_operacao.get()
        novo_data =  entry_data.get()
       
        if  novo_operacao and novo_data:
            try:
                    conn  =  conectar()
                    c = conn.cursor()
                    c.execute('UPDATE pecas SET operacao = ?,  data = ? WHERE lote = ?', (novo_operacao, novo_data,numero_lote))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo('Dados','DADOS INSERIDOS COM SUCESSO!')
                    mostra_peca()
                    entry_lote.delete(0, tk.END)
                    entry_operacao.delete(0, tk.END)
                    entry_data.delete(0, tk.END)
            except:
                    messagebox.showerror('Erro', 'OCORREU UM ERRO AO INSERIR OS DADOS, VERIFIQUE')
        else:
            messagebox.showwarning('Dado', 'INSIRA TODOS OS DADOS')





# DELETAR

def deletar_peca():
    selecao = tree.selection()
    if selecao:
        numero_lote  =  tree.item(selecao)['values'][0]
        conn  =  conectar()
        c = conn.cursor()
        c.execute('DELETE FROM pecas WHERE lote = ?', (numero_lote,))
        conn.commit()
        conn.close()
        messagebox.showinfo('Dados', 'DADOS DELETADOS COM SUCESSO!')
        mostra_peca()
    else:
        messagebox.showerror('Dados', 'ERRO AO DELETAR OS DADOS!')    
     
   


# interface grafica
janela = tk.Tk()
janela.geometry('800x500')
janela.title('VERIFÁCIL')

style = ttk.Style()
style.theme_use('clam')
style.configure('TLabel', background = 'white', font = ('arial', 10))
style.configure('TEntry', font = ('Segoe UI', 10))
style.configure('TButton', font = ('Segoe UI', 10), padding = 6)
style.configure('Treeview.Hending', font = ('Segoe UI', 10, 'bold'))
style.configure('Treeview',font = ('Segoe UI', 10, 'bold'))


# frames  -  sessão
main_frame =  ttk.Frame(janela, padding=15)
main_frame.pack(fill=tk.BOTH, expand=True)


# widgets -  elementos  

titulo = ttk.Label(main_frame, text='Sistema de Controle de Produção VeriFácil', font=('Segoe UI', 10, 'bold'))
titulo.grid(row=0, columnspan=2,pady=(0,15), sticky='w')
###############################

input_frame =  ttk.LabelFrame(main_frame, text='DADOS DA PEÇA', padding=10)
input_frame.grid(row=1,column= 0, columnspan = 2, sticky='ew', pady=(0,15))

# textos para direcionar
# CPF
ttk.Label(input_frame, text='NÚMERO DO LOTE').grid(row=0, column=0, padx=(0,10), pady=5, sticky='e')

entry_lote = ttk.Entry(input_frame, width=30)
entry_lote.grid(row=0, column=1, padx=(0,20), pady=5, sticky='w')

# textos para direcionar
# OPERACAO
ttk.Label(input_frame, text='OPERAÇÃO REALIZADA').grid(row=1, column=0, padx=(0,10), pady=5, sticky='e')

entry_operacao = ttk.Entry(input_frame, width=30)
entry_operacao.grid(row=1, column=1, padx=(0,20), pady=5, sticky='w')


# textos para direcionar
# DATA
ttk.Label(input_frame, text='DATA DO REGISTRO').grid(row=2, column=0, padx=(0,10), pady=5, sticky='e')

entry_data = ttk.Entry(input_frame, width=30)
entry_data.grid(row=2, column=1, padx=(0,20), pady=5, sticky='w')



#situacao
ttk.Label(input_frame, text='SITUAÇÃO DA PEÇA').grid(row=3, column=0, padx=(0,10), pady=5, sticky='e')
opcoes = ['Reprovada', 'Aprovada']
entry_situacao = ttk.Combobox(input_frame, width=30, values = opcoes)
entry_situacao.grid(row=3, column=1, padx=(0,20), pady=5, sticky='w')


# botões
btn_frame = ttk.Frame(main_frame)
btn_frame.grid(row=2, column=0, columnspan=2, pady=(0,15), sticky='ew')


btn_salvar = ttk.Button(btn_frame, text='SALVAR', command=inserir_peca)
btn_salvar.pack(side = tk.LEFT, padx=5 )

btn_atualizar = ttk.Button(btn_frame, text='ATUALIZAR', command=editar)
btn_atualizar.pack(side = tk.LEFT, padx=5 )

btn_deletar = ttk.Button(btn_frame, text='DELETAR', command= deletar_peca)
btn_deletar.pack(side = tk.LEFT, padx=5 )

# btn_limpar = ttk.Button(btn_frame, text='LIMPAR')
# btn_limpar.pack(side = tk.LEFT, padx=5 )

# Treeview - vizualizar os dados

tree_frame = ttk.Frame(main_frame)
tree_frame.grid(row=3, column=0, columnspan=2, sticky='nsew')

main_frame.columnconfigure(0, weight = 1)
main_frame.rowconfigure(3,weight = 1)

# criação da TreeView
columns = ('LOTE', 'OPERAÇÃO', 'DATA', 'SITUAÇÃO')
tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=12)
tree.pack(fill=tk.BOTH, expand=True)

for col in columns:
    tree.heading(col, text= col)
    tree.column(col, width=180, anchor='center')

# scrolbar -  barra rolagem

scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

criar_tabela()
mostra_peca()

janela.mainloop()