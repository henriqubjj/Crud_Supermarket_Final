import tkinter as tk
from tkinter import messagebox, Toplevel, Listbox
from gerenciador_crud import GerenciadorCRUD
from .login_window import LoginWindow
from .register_window import RegisterWindow

class MainWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("JampaSUL Supermercado")
        self.gerenciador_crud = GerenciadorCRUD()
        self.master.geometry("400x400")
        self.pack()
        self.create_widgets()
    
    def create_widgets(self):

        # Usando um Frame para agrupar os botões
        button_frame = tk.Frame(self)
        button_frame.pack(side="top", fill="x", pady=10)
        
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
        self.logout_button['state'] = tk.DISABLED
        messagebox.showinfo("Logout", "Você foi deslogado com sucesso.")

    def abrir_perfil(self):
        # Aqui você deve abrir a janela de perfil do usuário
        pass

