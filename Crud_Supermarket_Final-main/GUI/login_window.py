import tkinter as tk
from tkinter import messagebox


class LoginWindow(tk.Toplevel):
    def __init__(self, parent, gerenciador_crud):
        super().__init__(parent)
        self.gerenciador_crud = gerenciador_crud
        self.title("Login")
        self.geometry("300x200")
        self.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        # Label para e-mail
        self.label_email = tk.Label(self, text="E-mail:")
        self.label_email.pack(pady=(10, 0))

        # Campo de entrada para e-mail
        self.entry_email = tk.Entry(self)
        self.entry_email.pack()

        # Label para senha
        self.label_senha = tk.Label(self, text="Senha:")
        self.label_senha.pack(pady=(10, 0))

        # Campo de entrada para senha
        self.entry_senha = tk.Entry(self, show="*")
        self.entry_senha.pack()

        # Botão de login
        self.btn_login = tk.Button(self, text="Login", command=self.login)
        self.btn_login.pack(pady=(15, 0))

    def login(self):
        email = self.entry_email.get()
        senha = self.entry_senha.get()
        self.usuario_logado = self.gerenciador_crud.autenticar_usuario(email, senha)
        if self.usuario_logado:
            messagebox.showinfo("Login bem-sucedido", f"Bem-vindo {self.usuario_logado['nome']}!")
            self.destroy()  # Fecha a janela de login
        else:
            messagebox.showerror("Erro de login", "E-mail ou senha incorretos")
