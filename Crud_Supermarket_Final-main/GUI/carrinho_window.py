import tkinter as tk
from tkinter import messagebox

class CarrinhoWindow(tk.Toplevel):
    def __init__(self, master=None, carrinho=[]):
        super().__init__(master)
        self.master = master
        self.title("Meu Carrinho")
        self.geometry("400x300")
        self.carrinho = carrinho  # Carrinho recebido como parâmetro
        
        self.create_widgets()

    def create_widgets(self):
        # Lista de itens do carrinho
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.carrinho_listbox = tk.Listbox(self, yscrollcommand=self.scrollbar.set)
        self.carrinho_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.carrinho_listbox.yview)

        # Botão para remover item do carrinho
        self.remover_button = tk.Button(self, text="Remover Item", command=self.remover_item)
        self.remover_button.pack(side=tk.BOTTOM)

        # Preencher a lista com os itens do carrinho
        self.atualizar_carrinho()

    def atualizar_carrinho(self):
        self.carrinho_listbox.delete(0, tk.END)  # Limpar a lista antes de atualizar
        for item in self.carrinho:
            self.carrinho_listbox.insert(tk.END, f"{item['nome']} - R${item['preco']:.2f} - Quantidade: {item['quantidade']}")

    def remover_item(self):
        # Obter o índice do item selecionado na lista
        selected_index = self.carrinho_listbox.curselection()
        if selected_index:
            # Remover o item do carrinho com base no índice selecionado
            del self.carrinho[selected_index[0]]
            # Atualizar a lista após a remoção
            self.atualizar_carrinho()
            messagebox.showinfo("Remoção", "Item removido do carrinho com sucesso.")
        else:
            messagebox.showwarning("Seleção Inválida", "Selecione um item para remover.")