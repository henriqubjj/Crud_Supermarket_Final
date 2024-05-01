import tkinter as tk
from tkinter import messagebox, Toplevel, Listbox
from gerenciador_crud import GerenciadorCRUD
from .login_window import LoginWindow
from .register_window import RegisterWindow
from .CartWindow import CartWindow

class MainWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("JampaSUL Supermercado")
        self.gerenciador_crud = GerenciadorCRUD()
        self.master.geometry("500x500")
        self.usuario_logado = None
        self.pack()
        self.selected_items = []  # Armazena os itens selecionados para o carrinho
        self.create_widgets()
    
    def create_widgets(self):

        # Usando um Frame para agrupar os botões
        button_frame = tk.Frame(self)
        button_frame.pack(side="top", fill="x", pady=10)

        # Scrollbar
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Lista de produtos com seleção múltipla
        self.produtos_listbox = tk.Listbox(self, selectmode='multiple', yscrollcommand=self.scrollbar.set)
        self.produtos_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.produtos_listbox.yview)
        self.listar_produtos()
        
        # Campo de entrada para quantidade
        self.label_quantidade = tk.Label(button_frame, text="Quantidade:")
        self.label_quantidade.pack(side="left")
        self.entry_quantidade = tk.Entry(button_frame)
        self.entry_quantidade.pack(side="left")

        # Botão de login
        self.login_button = tk.Button(self, text="Sign in", command=self.login)
        self.login_button.pack(side="top")

        #Botão de casdro de usuario
        self.register_button = tk.Button(button_frame, text="Sign up", command=self.register_user)
        self.register_button.pack(side="left", padx=10, pady=5)


        # Botão de logout, inicialmente desabilitado
        self.logout_button = tk.Button(button_frame, text="Logout", state="disabled", command=self.logout)
        self.logout_button.pack(side="left")
        
        # Botão de perfil de usuário
        self.perfil_button = tk.Button(button_frame, text="Perfil", state="disabled", command=self.abrir_perfil)
        self.perfil_button.pack(side="left")

        # Botão Carrinho
        self.cart_button = tk.Button(self, text="Carrinho", state=tk.DISABLED, command=self.open_cart)
        self.cart_button.pack(side="top")

        # Botão para adicionar ao carrinho
        self.add_to_cart_button = tk.Button(self, text="Adicionar ao Carrinho", state=tk.DISABLED, command=self.add_to_cart)
        self.add_to_cart_button.pack(side="top")
        
    def listar_produtos(self):
        self.produtos_listbox.delete(0, tk.END)
        # Obter e listar produtos
        produtos = self.gerenciador_crud.listar_produtos()
        for produto in produtos:
            self.produtos_listbox.insert(tk.END, f"{produto[1]} - R$ {produto[2]:.2f}")

    def add_to_cart(self):
        selected_index = self.produtos_listbox.curselection()
        if selected_index:
            selected_product = self.produtos_listbox.get(selected_index)
            quantity = int(self.entry_quantidade.get()) if self.entry_quantidade.get().isdigit() else 0
            if quantity > 0:
                self.selected_items.append((selected_product, quantity))
                messagebox.showinfo("Carrinho", f"{quantity} unidades de {selected_product.split('-')[0]} adicionadas ao carrinho!")
            else:
                messagebox.showerror("Erro", "Quantidade inválida.")
        else:
            messagebox.showerror("Erro", "Selecione um produto para adicionar.")

    def open_cart(self):
        if self.selected_items:
            cart_window = CartWindow(self, self.selected_items)
            self.wait_window(cart_window)
        else:
            messagebox.showinfo("Carrinho", "O carrinho está vazio!")

    def register_user(self):
        # Aqui você abrirá a janela de cadastro de usuário
        register_window = RegisterWindow(self, self.gerenciador_crud)
        self.register_button['state'] = tk.DISABLED  # Desabilita o botão de registro
        self.wait_window(register_window)  # Espera até que a janela de registro seja fechada
        self.register_button['state'] = tk.NORMAL  # Reabilita o botão de registro após fechar a janela de registro
        self.wait_window(register_window)
        print("Abrir janela de cadastro de usuário...")  # Placeholder para a janela de cadastro real


    def login(self):
        # Chamando a janela de login
        login_window = LoginWindow(self, self.gerenciador_crud)
        self.login_button['state'] = tk.DISABLED  # Desabilita o botão de login
        self.wait_window(login_window)  # Espera até que a janela de login seja fechada
        self.login_button['state'] = tk.NORMAL  # Reabilita o botão de login após fechar a janela de login

        # Aqui você pode adicionar lógica adicional após o login ser concluído,
        # por exemplo, atualizar a interface com informações do usuário logado.

        pass

    def logout(self):
        if messagebox.askyesno("Logout", "Você deseja deslogar?"):
            self.update_login_state(False)  # Atualiza o estado de login
            messagebox.showinfo("Logout", "Você foi deslogado com sucesso.")


    def abrir_perfil(self):
        # Aqui você deve abrir a janela de perfil do usuário
        pass

    def update_login_state(self, logged_in):
        if logged_in:
            self.logout_button['state'] = tk.NORMAL
            self.perfil_button['state'] = tk.NORMAL
            self.login_button['state'] = tk.DISABLED
            self.register_button['state'] = tk.DISABLED
            self.cart_button['state'] = tk.NORMAL
            self.add_to_cart_button['state'] = tk.NORMAL
        else:
            # Habilita botões de login e sign up ao deslogar
            self.login_button['state'] = tk.NORMAL
            self.register_button['state'] = tk.NORMAL
            self.logout_button['state'] = tk.DISABLED
            self.perfil_button['state'] = tk.DISABLED
            self.usuario_logado = None
            self.cart_button['state'] = tk.DISABLED
            self.add_to_cart_button['state'] = tk.DISABLED
            self.selected_items.clear()  # Limpa o carrinho ao deslogar



