from flask import Flask
import app.models.Heart as Heart


# Função para criar um funcionário usado em app/controllers/default.py
def criar_funcionario(nome, cpf, nascimento, admissao):
    funcionario = Heart.Funcionarios(
        Nome=nome,
        Nascimento=nascimento,
        CPF=cpf,
        Admissao=admissao
    )
    empresa.contratar_funcionario(funcionario)
    return "Funcionário cadastrado com sucesso!"


# Função para demitir um funcionário usado em app/controllers/default.py
def demitir_funcionario(cpf):
    empresa.demitir_funcionario(cpf)
    return "Funcionário demitido com sucesso!"


# Função p/ definir cargo de um funcionário usado em app/controllers/default.py
def definir_cargo_funcionario(cpf, cargo):
    empresa.definir_cargo_funcionario(cpf, cargo)
    return "Cargo definido com sucesso!"


app = Flask(__name__)  # Cria uma instância do Flask


'''Criação de cargos

As opções de cargos devem ser criadas antes da empresa ser criada
Deve seguir a estrutura abaixo:

lista_de_cargos = [
    Heart.Cargos("Nome do cargo", Salário)
]
'''
lista_cargos = [
    Heart.Cargos("Caixa", 1500),        # 0
    Heart.Cargos("Gerente", 5000),      # 1
    Heart.Cargos("Faxineiro", 1000),    # 2
    Heart.Cargos("Vendedor", 2000),     # 3
    Heart.Cargos("Diretor", 10000)      # 4
]

'''Criação da empresa

Deve seguir a estrutura abaixo:

empresa = Heart.Empresa(
    nome="Nome da empresa",
    link_fb='exemplo-48483-default-rtdb',
    cargos=lista_de_cargos
)
'''
empresa = Heart.Empresa(
    nome="Projeto Python",
    link_fb='exemplo-48483-default-rtdb',
    cargos=lista_cargos
)


# Importa o arquivo default.py que contém as rotas da aplicação
from app.controllers import default  # noqa E402
