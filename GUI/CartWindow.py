import tkinter as tk
from tkinter import messagebox

class CartWindow(tk.Toplevel):
    def __init__(self, parent, items):
        super().__init__(parent)
        self.title("Carrinho de Compras")
        self.geometry("300x300")
        self.resizable(False, False)
        self.parent = parent
        self.items = items
        self.create_widgets()

    def create_widgets(self):
        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        for item in self.items:
            self.listbox.insert(tk.END, item)

        # Botão para finalizar compra
        self.checkout_button = tk.Button(self, text="Finalizar Compra", command=self.checkout)
        self.checkout_button.pack(side="bottom")

        # Adiciona itens ao listbox
        self.update_listbox()
        
        # Botão para limpar o carrinho
        self.clear_cart_button = tk.Button(self, text="Limpar Carrinho", command=self.clear_cart)
        self.clear_cart_button.pack(side="top", padx=10, pady=5)


    def clear_cart(self):
        # Limpa todos os itens do carrinho
        if messagebox.askyesno("Limpar Carrinho", "Tem certeza que deseja limpar o carrinho?"):
            self.items.clear()  # Limpa a lista de itens
            self.update_listbox()  # Atualiza a interface do listbox
            messagebox.showinfo("Carrinho", "O carrinho foi limpo com sucesso.")

    def update_listbox(self):
        # Limpa o listbox e adiciona itens atualizados
        self.listbox.delete(0, tk.END)
        for item, quantity in self.items:
            self.listbox.insert(tk.END, f"{item} - Quantidade: {quantity}")

    def checkout(self):
        # Implemente a lógica para finalizar a compra
        messagebox.showinfo("Compra", "Compra finalizada com sucesso!")
        self.destroy()
