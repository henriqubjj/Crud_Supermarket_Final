import tkinter as tk
from tkinter import messagebox, Toplevel, Listbox, Checkbutton
from gerenciador_crud import GerenciadorCRUD
from .login_window import LoginWindow
from .register_window import RegisterWindow
from .carrinho_window import CarrinhoWindow

class MainWindow(tk.Frame):
    def __init__(self, master=None, gerenciador_crud=None):
        super().__init__(master)
        self.master = master
        self.master.title("JampaSUL Supermercado")
        self.gerenciador_crud = gerenciador_crud if gerenciador_crud else GerenciadorCRUD()  # Use o objeto existente ou crie um novo
        self.master.geometry("400x400")
        self.pack()
        self.create_widgets()
        
        self.carrinho_ = [] # Lista para armazenar os itens do carrinho
        self.produtos = [] # Adiciona esta linha para armazenar os produtos   


    def create_widgets(self):
        # Usando um Frame para agrupar os botões
        button_frame = tk.Frame(self)
        button_frame.pack(side="top", fill="x", pady=10)
        
        # Botão de login
        self.login_button = tk.Button(self, text="Entrar", command=self.login)
        self.login_button.pack(side="top")

        #Botão de cadastro
        self.register_button = tk.Button(button_frame, text="Cadastrar-se", command=self.register_user)
        self.register_button.pack(side="left", padx=10, pady=5)

        #Botao de sair
        self.logout_button = tk.Button(button_frame, text="Sair", state="disabled", command=self.logout)
        self.logout_button.pack(side="left")
        
        #Botao do carrinho
        self.carrinho_button = tk.Button(button_frame, text="Meu carrinho", state="active", command=self.carrinho_de_compras)
        self.carrinho_button.pack(side="left")

        # Botão de perfil de usuário
        self.perfil_button = tk.Button(button_frame, text="Perfil", state="disabled", command=self.abrir_perfil)
        self.perfil_button.pack(side="left")

        # Lista de produtos
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.produtos_listbox = tk.Listbox(self, yscrollcommand=self.scrollbar.set)
        self.produtos_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.produtos_listbox.yview)
        self.listar_produtos()
    


    def listar_produtos(self):
        # Obter e listar produtos
        produtos = self.gerenciador_crud.listar_produtos()
        for produto in produtos:
            self.produtos_listbox.insert(tk.END, f"{produto[1]} - R$ {produto[2]:.2f} - Em estoque: {produto[4]}")
            

    def register_user(self):
        # Aqui você abrirá a janela de cadastro de usuário
        register_window = RegisterWindow(self, self.gerenciador_crud)
        self.register_button['state'] = tk.DISABLED  # Desabilita o botão de registro
        self.wait_window(register_window)  # Espera até que a janela de registro seja fechada
        self.register_button['state'] = tk.NORMAL  # Reabilita o botão de registro após fechar a janela de registro
    
    def carrinho_de_compras(self):
        # Chamando a janela do carrinho
        carrinho_window = CarrinhoWindow()
        self.carrinho_button['state'] = tk.DISABLED  # Desabilita o botão de login
        self.wait_window(carrinho_window)  # Espera até que a janela de login seja fechada
        self.carrinho_button['state'] = tk.NORMAL  # Reabilita o botão de login após fechar a janela de login


    def login(self):
        # Chamando a janela de login
        login_window = LoginWindow(self, self.gerenciador_crud)
        self.login_button['state'] = tk.DISABLED  # Desabilita o botão de login
        self.wait_window(login_window)  # Espera até que a janela de login seja fechada
        self.login_button['state'] = tk.NORMAL  # Reabilita o botão de login após fechar a janela de login
        if self.gerenciador_crud.verificar_autenticacao():
            self.logout_button['state'] = tk.NORMAL

    def logout(self):
        if self.gerenciador_crud.retornar_usuario():
            messagebox.showinfo("Saindo", f"Até a próxima {self.gerenciador_crud.retornar_usuario()['nome']}!")
        self.gerenciador_crud.logout()
        self.logout_button['state'] = tk.DISABLED

    def abrir_perfil(self):
        # Aqui você deve abrir a janela de perfil do usuário
        pass

