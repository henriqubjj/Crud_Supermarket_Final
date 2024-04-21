import sqlite3
from datetime import datetime

class GerenciadorCRUD:
    def __init__(self, db_name="supermercado.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.setup_database()
        self.usuario_logado = None

    def setup_database(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL,
                senha TEXT NOT NULL,
                telefone TEXT,
                endereco TEXT,
                is_flamengo INTEGER DEFAULT 0,
                watch_one_piece INTEGER DEFAULT 0,
                is_de_sousa INTEGER DEFAULT 0,
                is_funcionario INTEGER DEFAULT 0
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                preco REAL NOT NULL,
                categoria TEXT NOT NULL,
                quantidade_estoque INTEGER NOT NULL,
                fabricado_em_mari INTEGER DEFAULT 0
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS compras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER,
                vendedor_id INTEGER,
                data TEXT,
                forma_pagamento TEXT,
                total REAL,
                FOREIGN KEY(cliente_id) REFERENCES usuarios(id),
                FOREIGN KEY(vendedor_id) REFERENCES usuarios(id)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS itens_compra (
                compra_id INTEGER,
                produto_id INTEGER,
                quantidade INTEGER,
                FOREIGN KEY(compra_id) REFERENCES compras(id),
                FOREIGN KEY(produto_id) REFERENCES produtos(id)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS funcionarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL,
                senha TEXT NOT NULL,
                cargo TEXT NOT NULL,
                salario REAL NOT NULL
            )
        ''')
        self.connection.commit()

    def adicionar_usuario(self, nome, email, senha, telefone, endereco, is_flamengo=0, watch_one_piece=0, is_de_sousa=0, is_funcionario=0):
        self.cursor.execute("INSERT INTO usuarios (nome, email, senha, telefone, endereco, is_flamengo, watch_one_piece, is_de_sousa, is_funcionario) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                            (nome, email,senha, telefone, endereco, is_flamengo, watch_one_piece, is_de_sousa, is_funcionario))
        self.connection.commit()
        print(f"Usuário '{nome}' adicionado com sucesso.")

    def listar_usuarios(self):
        self.cursor.execute("SELECT * FROM usuarios")
        usuarios = self.cursor.fetchall()
        print("Listagem de todos os usuários:")
        for usuario in usuarios:
            print(f"ID: {usuario[0]}, Nome: {usuario[1]}, Telefone: {usuario[3]}, Endereço: {usuario[4]}")
        print("--------------------------")
        return usuarios

    def pesquisar_usuarios_por_nome(self, nome):
        self.cursor.execute("SELECT * FROM usuarios WHERE nome LIKE ?", ('%' + nome + '%',))
        usuarios = self.cursor.fetchall()
        print(f"Resultados da pesquisa por nome '{nome}':")
        for usuario in usuarios:
            print(f"ID: {usuario[0]}, Nome: {usuario[1]}")
        return usuarios

    def exibir_usuario(self, id):
        self.cursor.execute("SELECT id, nome, senha, telefone, endereco, is_flamengo, watch_one_piece, is_de_sousa, is_funcionario FROM usuarios WHERE id = ?", (id,))
        row = self.cursor.fetchone()
        if row:
            columns = ['id', 'nome', 'senha', 'telefone', 'endereco', 'is_flamengo', 'watch_one_piece', 'is_de_sousa', 'is_funcionario']
            usuario = dict(zip(columns, row))
            print(f"Detalhes do usuário ID {usuario['id']}: Nome: {usuario['nome']}, Telefone: {usuario['telefone']}, Endereço: {usuario['endereco']}")
            return usuario
        else:
            print(f"Usuário com ID {id} não encontrado.")
            return None

    def remover_usuario(self, id):
        self.cursor.execute("DELETE FROM usuarios WHERE id = ?", (id,))
        self.connection.commit()
        print(f"Usuário com ID {id} removido com sucesso.")

    def atualizar_usuario(self, id, nome=None, senha=None, telefone=None, endereco=None):
        updates = []
        parameters = []
        if nome:
            updates.append("nome = ?")
            parameters.append(nome)
        if senha:
            updates.append("senha = ?")
            parameters.append(senha)
        if telefone:
            updates.append("telefone = ?")
            parameters.append(telefone)
        if endereco:
            updates.append("endereco = ?")
            parameters.append(endereco)
        parameters.append(id)
        update_sql = "UPDATE usuarios SET " + ", ".join(updates) + " WHERE id = ?"
        self.cursor.execute(update_sql, parameters)
        self.connection.commit()
        print(f"Usuário com ID {id} atualizado com sucesso.")

    def autenticar_usuario(self, usuario_id, senha):
        self.cursor.execute("SELECT * FROM usuarios WHERE id = ? AND senha = ?", (usuario_id, senha))
        usuario = self.cursor.fetchone()
        if usuario:
            print(f"Usuário {usuario['nome']} autenticado com sucesso.")
            return usuario
        else:
            print("Falha na autenticação. Verifique as credenciais.")
            return None

    def adicionar_produto(self, nome, preco, categoria, quantidade_estoque):
        self.cursor.execute("INSERT INTO produtos (nome, preco, categoria, quantidade_estoque) VALUES (?, ?, ?, ?)", 
                            (nome, preco, categoria, quantidade_estoque))
        self.connection.commit()
        print(f"Produto '{nome}' adicionado com sucesso.")

    def remover_produto(self, id):
        self.cursor.execute("DELETE FROM produtos WHERE id = ?", (id,))
        self.connection.commit()
        print(f"Produto com ID {id} removido com sucesso.")

    def atualizar_produto(self, id, nome=None, preco=None, categoria=None, quantidade_estoque=None):
        updates = []
        parameters = []
        if nome:
            updates.append("nome = ?")
            parameters.append(nome)
        if preco is not None:
            updates.append("preco = ?")
            parameters.append(preco)
        if categoria:
            updates.append("categoria = ?")
            parameters.append(categoria)
        if quantidade_estoque is not None:
            updates.append("quantidade_estoque = ?")
            parameters.append(quantidade_estoque)
        parameters.append(id)
        update_sql = "UPDATE produtos SET " + ", ".join(updates) + " WHERE id = ?"
        self.cursor.execute(update_sql, parameters)
        self.connection.commit()
        print(f"Produto com ID {id} atualizado com sucesso.")

    def exibir_produto(self, produto_id):
        self.cursor.execute("SELECT id, nome, preco, categoria, quantidade_estoque FROM produtos WHERE id = ?", (produto_id,))
        produto = self.cursor.fetchone()
        if produto:
            # Construir um dicionário para tornar o acesso mais intuitivo
            produto_dict = {
                'id': produto[0],
                'nome': produto[1],
                'preco': produto[2],
                'categoria': produto[3],
                'quantidade_estoque': produto[4]
            }
            print(f"Produto encontrado: {produto_dict['nome']} com preço R${produto_dict['preco']:.2f} e quantidade em estoque: {produto_dict['quantidade_estoque']}")
            return produto_dict
        else:
            print(f"Produto com ID {produto_id} não encontrado.")
            return None

    def listar_produtos(self):
        self.cursor.execute("SELECT * FROM produtos")
        produtos = self.cursor.fetchall()
        print("Listagem de todos os produtos:")
        for produto in produtos:
            print(f"ID: {produto[0]}, Nome: {produto[1]}, Preço: {produto[2]}, Categoria: {produto[3]}, Estoque: {produto[4]}")
        return produtos

    def pesquisar_produto_por_nome(self, nome):
        self.cursor.execute("SELECT * FROM produtos WHERE nome LIKE ?", ('%' + nome + '%',))
        produtos = self.cursor.fetchall()
        print(f"Resultados da pesquisa por nome '{nome}':")
        for produto in produtos:
            print(f"ID: {produto[0]}, Nome: {produto[1]}")
        return produtos
    
    def adicionar_funcionario(self, nome, email, senha, cargo, salario):
        self.cursor.execute("INSERT INTO funcionarios (nome, email, senha, cargo, salario) VALUES (?, ?, ?, ?, ?)", 
                            (nome, email, senha, cargo, salario))
        self.connection.commit()
        print(f"Funcionário '{nome}' adicionado com sucesso ao sistema.")

    def listar_funcionarios(self):
        self.cursor.execute("SELECT * FROM funcionarios")
        funcionarios = self.cursor.fetchall()
        print("Listagem de todos os funcionários:")
        for funcionario in funcionarios:
            print(f"ID: {funcionario[0]}, Nome: {funcionario[1]}, Cargo: {funcionario[3]}, Salário: {funcionario[4]}")
        return funcionarios

    def remover_funcionario(self, id):
        self.cursor.execute("DELETE FROM funcionarios WHERE id = ?", (id,))
        self.connection.commit()
        print(f"Funcionário com ID {id} removido com sucesso.")

    def atualizar_funcionario(self, id, nome=None, senha=None, cargo=None, salario=None):
        updates = []
        parameters = []
        if nome:
            updates.append("nome = ?")
            parameters.append(nome)
        if senha:
            updates.append("senha = ?")
            parameters.append(senha)
        if cargo:
            updates.append("cargo = ?")
            parameters.append(cargo)
        if salario is not None:
            updates.append("salario = ?")
            parameters.append(salario)
        parameters.append(id)
        update_sql = "UPDATE funcionarios SET " + ", ".join(updates) + " WHERE id = ?"
        self.cursor.execute(update_sql, parameters)
        self.connection.commit()
        print(f"Funcionário com ID {id} atualizado com sucesso.")

    def pesquisar_funcionario_por_nome(self, nome):
        self.cursor.execute("SELECT * FROM funcionarios WHERE nome LIKE ?", ('%' + nome + '%',))
        funcionarios = self.cursor.fetchall()
        print(f"Resultados da pesquisa por nome '{nome}':")
        for funcionario in funcionarios:
            print(f"ID: {funcionario[0]}, Nome: {funcionario[1]}")
        return funcionarios

    def exibir_funcionario(self, id):
        self.cursor.execute("SELECT id, nome, senha, cargo, salario FROM funcionarios WHERE id = ?", (id,))
        funcionario = self.cursor.fetchone()
        if funcionario:
            funcionario_dict = {
                'id': funcionario[0],
                'nome': funcionario[1],
                'senha': funcionario[2],
                'cargo': funcionario[3],
                'salario': funcionario[4]
            }
            print(f"Detalhes do Funcionário ID {funcionario_dict['id']}: Nome: {funcionario_dict['nome']}, Cargo: {funcionario_dict['cargo']}, Salário: R${funcionario_dict['salario']:.2f}")
            return funcionario_dict
        else:
            print(f"Funcionário com ID {id} não encontrado.")
            return None

    
    def autenticar_funcionario(self, funcionario_id, senha):
        self.cursor.execute("SELECT * FROM usuarios WHERE id = ? AND senha = ? AND is_funcionario = 1", (funcionario_id, senha))
        funcionario = self.cursor.fetchone()
        if funcionario:
            print(f"Funcionário {funcionario['nome']} autenticado com sucesso.")
            return funcionario
        else:
            print("Falha na autenticação. Verifique as credenciais ou as permissões de funcionário.")
            return None
        
    def listar_vendedores(self):
        self.cursor.execute("SELECT * FROM funcionarios WHERE cargo = 'Vendedor'")
        vendedores = self.cursor.fetchall()
        print("Listagem de todos os vendedores:")
        for vendedor in vendedores:
            print(f"ID: {vendedor[0]}, Nome: {vendedor[1]}, Salário: {vendedor[4]}")
        return vendedores

    def exibir_vendedor(self, id):
        self.cursor.execute("SELECT * FROM funcionarios WHERE id = ? AND cargo = 'Vendedor'", (id,))
        vendedor = self.cursor.fetchone()
        if vendedor:
            print(f"Detalhes do Vendedor ID {id}: Nome: {vendedor[1]}, Salário: {vendedor[4]}")
        else:
            print(f"Vendedor com ID {id} não encontrado.")
        return vendedor
    
    def login(self, email, senha):
        # Tenta logar como usuário comum
        self.cursor.execute("SELECT id, nome FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
        usuario = self.cursor.fetchone()
        if usuario:
            self.usuario_logado = {'id': usuario[0], 'nome': usuario[1], 'tipo': 'usuario'}
            print(f"Usuário {usuario[1]} logado com sucesso.")
            return True
        
        # Tenta logar como funcionário
        self.cursor.execute("SELECT id, nome FROM funcionarios WHERE email = ? AND senha = ?", (email, senha))
        funcionario = self.cursor.fetchone()
        if funcionario:
            self.usuario_logado = {'id': funcionario[0], 'nome': funcionario[1], 'tipo': 'funcionario'}
            print(f"Funcionário {funcionario[1]} logado com sucesso.")
            return True

        print("Falha no login. ID ou senha incorretos.")
        return False

    def logout(self):
        if self.usuario_logado:
            print(f"{self.usuario_logado['nome']} deslogado com sucesso.")
            self.usuario_logado = None
        else:
            print("Nenhum usuário estava logado.")


    def realizar_compra(self,funcionario_id, forma_pagamento):
        if not self.usuario_logado or self.usuario_logado['tipo'] != 'usuario':
            print("Erro: Apenas usuários logados podem realizar compras.")
            return
        
        # Verificar se o funcionario é válido e tem o cargo 'Vendedor'
        vendedor = self.exibir_funcionario(funcionario_id)
        if not vendedor or vendedor['cargo'] != 'Vendedor':
            print(f"Erro: O ID {funcionario_id} não corresponde a um vendedor válido. Compra não pode ser realizada.")
            return

        # Preparando a compra
        total = 0
        itens_compra = []

        # Loop para adicionar produtos à compra
        while True:
            produto_id = int(input("Digite o ID do produto que deseja comprar (0 para finalizar): "))
            if produto_id == 0:
                break
            quantidade = int(input("Digite a quantidade que deseja comprar: "))

            produto = self.exibir_produto(produto_id)
            if not produto or produto['quantidade_estoque'] < quantidade:
                print(f"Erro: Estoque insuficiente para o produto {produto['nome']}.")
                continue

            preco_total_produto = produto['preco'] * quantidade
            if self.usuario_logado['tipo'] == 'usuario' and (self.usuario_logado.get('is_flamengo') or self.usuario_logado.get('watch_one_piece') or self.usuario_logado.get('is_de_sousa')):
                desconto = 0.15 * preco_total_produto
                preco_total_produto -= desconto
                print(f"Desconto aplicado de 15%: -R${desconto:.2f}")

            total += preco_total_produto
            itens_compra.append((produto_id, quantidade, preco_total_produto))
            print(f"Produto {produto['nome']} adicionado à compra. Subtotal: R${preco_total_produto:.2f}")

        # Confirmação final da compra
        print(f"Total da compra: R${total:.2f}")
        confirmacao = input("Confirmar compra? (sim/não): ")
        if confirmacao.lower() != 'sim':
            print("Compra cancelada pelo usuário.")
            return

        # Inserindo a compra no banco de dados
        self.cursor.execute("INSERT INTO compras (cliente_id, vendedor_id, data, forma_pagamento, total) VALUES (?, ?, ?, ?, ?)",
                            (self.usuario_logado, funcionario_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), forma_pagamento, total))
        compra_id = self.cursor.lastrowid

        # Atualizando estoque e inserindo itens da compra
        for item in itens_compra:
            produto_id, quantidade, _ = item
            self.cursor.execute("UPDATE produtos SET quantidade_estoque = quantidade_estoque - ? WHERE id = ?", (quantidade, produto_id))
            self.cursor.execute("INSERT INTO itens_compra (compra_id, produto_id, quantidade) VALUES (?, ?, ?)", (compra_id, produto_id, quantidade))
        self.connection.commit()
        print("Compra realizada com sucesso.")

    def relatorio_vendas(self):
        self.cursor.execute("""
            SELECT vendedor_id, COUNT(*) as num_vendas, SUM(total) as valor_total
            FROM compras
            GROUP BY vendedor_id
        """)
        vendas = self.cursor.fetchall()
        print("Relatório de Vendas por Vendedor:")
        if vendas:
            for venda in vendas:
                print(f"Vendedor ID: {venda[0]}, Número de Vendas: {venda[1]}, Valor Total: R${venda[2]:.2f}")
        else:
            print("Nenhum dado de venda encontrado.")
        return vendas

    def relatorio_estoque(self):
        self.cursor.execute("""
            SELECT categoria, SUM(quantidade_estoque) as total_estoque
            FROM produtos
            GROUP BY categoria
        """)
        estoques = self.cursor.fetchall()
        print("Relatório de Estoque por Categoria:")
        if estoques:
            for estoque in estoques:
                print(f"Categoria: {estoque[0]}, Total em Estoque: {estoque[1]} unidades")
        else:
            print("Nenhum dado de estoque encontrado.")
        return estoques

    def relatorio_usuarios(self):
        self.cursor.execute("""
            SELECT COUNT(*) as total_usuarios, SUM(is_flamengo) as flamengo_fans,
                   SUM(watch_one_piece) as one_piece_watchers, SUM(is_de_sousa) as sousa_residents
            FROM usuarios
        """)
        usuarios = self.cursor.fetchone()
        print("Relatório de Usuários:")
        print(f"Total de Usuários: {usuarios[0]}")
        print(f"Torcedores do Flamengo: {usuarios[1]}")
        print(f"Fãs de One Piece: {usuarios[2]}")
        print(f"Residentes de Sousa: {usuarios[3]}")
        return usuarios
    
    def visualizar_perfil(self, usuario_id):
        usuario = self.exibir_usuario(usuario_id)
        if not usuario:
            print("Erro: Nenhum usuário logado ou usuário não encontrado.")
            return

        # Exibição dos dados do usuário
        print("Detalhes do Perfil:")
        print(f"ID: {usuario['id']}")
        print(f"Nome: {usuario['nome']}")
        print(f"Telefone: {usuario['telefone']}")
        print(f"Endereço: {usuario['endereco']}")
        print(f"Torcedor do Flamengo: {'Sim' if usuario['is_flamengo'] else 'Não'}")
        print(f"Assiste One Piece: {'Sim' if usuario['watch_one_piece'] else 'Não'}")
        print(f"É de Sousa: {'Sim' if usuario['is_de_sousa'] else 'Não'}")
        print(f"Funcionário: {'Sim' if usuario['is_funcionario'] else 'Não'}")

        # Exibição das compras realizadas pelo usuário
        self.cursor.execute("SELECT id, data, forma_pagamento, total FROM compras WHERE cliente_id = ?", (usuario_id,))
        compras = self.cursor.fetchall()
        if compras:
            print("Compras Realizadas:")
            for compra in compras:
                print(f"Compra ID: {compra[0]}, Data: {compra[1]}, Forma de Pagamento: {compra[2]}, Total: R${compra[3]:.2f}")
        else:
            print("Nenhuma compra registrada.")
        
    def pesquisar_produtos_baixo_estoque(self, funcionario_id, senha):
        # Verificar se o usuário é um funcionário e está autenticado corretamente
        if self.autenticar_funcionario(funcionario_id, senha):
            self.cursor.execute("SELECT * FROM produtos WHERE quantidade_estoque < 5")
            produtos = self.cursor.fetchall()
            print("Produtos com baixo estoque (<5 unidades):")
            if produtos:
                for produto in produtos:
                    print(f"Produto ID: {produto[0]}, Nome: {produto[1]}, Estoque: {produto[4]} unidades")
            else:
                print("Todos os produtos têm estoque suficiente.")
        else:
            print("Acesso negado. Verificação de credenciais falhou ou o usuário não é um funcionário.")





