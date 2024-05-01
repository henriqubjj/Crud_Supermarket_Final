import tkinter as tk
from tkinter import messagebox, IntVar

class RegisterWindow(tk.Toplevel):
    def __init__(self, parent, gerenciador_crud):
        super().__init__(parent)
        self.gerenciador_crud = gerenciador_crud
        self.title("Cadastro de Usuário")
        self.geometry("400x600")
        self.resizable(False, False)
        self.is_flamengo = IntVar(value=0)
        self.watch_one_piece = IntVar(value=0)
        self.is_de_sousa = IntVar(value=0)
        self.create_widgets()
        self.create_promotion_options()

    def create_widgets(self):
        # Criar e posicionar os campos de entrada para os dados do usuário
        self.label_nome = tk.Label(self, text="Nome:")
        self.label_nome.pack(pady=(10, 0))
        self.entry_nome = tk.Entry(self)
        self.entry_nome.pack()

        self.label_email = tk.Label(self, text="Email:")
        self.label_email.pack(pady=(10, 0))
        self.entry_email = tk.Entry(self)
        self.entry_email.pack()

        self.label_senha = tk.Label(self, text="Senha:")
        self.label_senha.pack(pady=(10, 0))
        self.entry_senha = tk.Entry(self, show="*")
        self.entry_senha.pack()

        self.label_telefone = tk.Label(self, text="Telefone:")
        self.label_telefone.pack(pady=(10, 0))
        self.entry_telefone = tk.Entry(self)
        self.entry_telefone.pack()

        self.label_endereco = tk.Label(self, text="Endereço:")
        self.label_endereco.pack(pady=(10, 0))
        self.entry_endereco = tk.Entry(self)
        self.entry_endereco.pack()


        # Opções is_flamengo
        self.label_flamengo = tk.Label(self, text="Torcedor do Flamengo?")
        self.label_flamengo.pack()
        tk.Radiobutton(self, text="Sim", variable=self.is_flamengo, value=1).pack()
        tk.Radiobutton(self, text="Não", variable=self.is_flamengo, value=0).pack()

        # Opções watch_one_piece
        self.label_one_piece = tk.Label(self, text="Assiste One Piece?")
        self.label_one_piece.pack()
        tk.Radiobutton(self, text="Sim", variable=self.watch_one_piece, value=1).pack()
        tk.Radiobutton(self, text="Não", variable=self.watch_one_piece, value=0).pack()

        # Opções is_de_sousa
        self.label_de_sousa = tk.Label(self, text="É de Sousa?")
        self.label_de_sousa.pack()
        tk.Radiobutton(self, text="Sim", variable=self.is_de_sousa, value=1).pack()
        tk.Radiobutton(self, text="Não", variable=self.is_de_sousa, value=0).pack()

        # Botões de cadastro e cancelamento
        self.btn_cadastrar = tk.Button(self, text="Cadastrar", command=self.register)
        self.btn_cadastrar.pack(pady=(15, 10))

        self.btn_cancelar = tk.Button(self, text="Cancelar", command=self.destroy)
        self.btn_cancelar.pack()

    def register(self):
        # Coleta os dados do formulário
        nome = self.entry_nome.get()
        email = self.entry_email.get()
        senha = self.entry_senha.get()
        telefone = self.entry_telefone.get()
        endereco = self.entry_endereco.get()
        flamengo = self.is_flamengo.get()
        one_piece = self.watch_one_piece.get()
        de_sousa = self.is_de_sousa.get()

        try:
            # ... lógica para adicionar o usuário ...
            self.gerenciador_crud.adicionar_usuario(
                nome, email, senha, telefone, endereco,
                is_flamengo=flamengo,
                watch_one_piece=one_piece,
                is_de_sousa=de_sousa
            )
        except Exception as e:
            messagebox.showerror("Erro", str(e))
