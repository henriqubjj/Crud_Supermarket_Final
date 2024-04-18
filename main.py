from classes import *

crud = GerenciadorCRUD()

# Cadastrando 3 produtos diferentes
#crud.adicionar_produto(nome="Arroz", preco=19.99, categoria="Alimentos", quantidade_estoque=150)
#crud.adicionar_produto(nome="Feijão", preco=14.49, categoria="Alimentos", quantidade_estoque=200)
#crud.adicionar_produto(nome="Macarrão", preco=5.99, categoria="Alimentos", quantidade_estoque=180)

# Cadastrando um usuário
#usuario_id = crud.adicionar_usuario(nome="João Silva", senha="1234", telefone="123456789", endereco="Rua das Flores 123", is_flamengo=1, watch_one_piece=1, is_de_sousa=0, is_funcionario=0)
#crud.listar_usuarios()

#Cadastrando um funcionario(vendedor)
#crud.adicionar_funcionario("Marcos", "marcos123", "Vendedor", 4000.00)
#crud.listar_funcionarios()

#Realizar login
crud.login(1,"1234")

#Realizar Logout
#crud.logout()

#Realizando a compra de 1 dos itens
crud.realizar_compra(funcionario_id=3,forma_pagamento="pix")




