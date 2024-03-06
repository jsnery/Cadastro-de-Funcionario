import app.models.Heart as Heart
from flask import Flask, render_template, request, jsonify


def criar_funcionario(nome, cpf, nascimento, contratacao): # Função para criar um funcionário usado em app/controllers/default.py
    funcionario = Heart.Funcionarios(nome, nascimento, cpf, contratacao)
    empresa.contratar_funcionario(funcionario)
    return "Funcionário cadastrado com sucesso!"

def demitir_funcionario(cpf): # Função para demitir um funcionário usado em app/controllers/default.py
    empresa.demitir_funcionario(cpf)
    return "Funcionário demitido com sucesso!"

def definir_cargo_funcionario(cpf, cargo): # Função para definir o cargo de um funcionário usado em app/controllers/default.py
    empresa.definir_cargo_funcionario(cpf, cargo)
    return "Cargo definido com sucesso!"

app = Flask(__name__)


''' 
Criação de cargos

As opções de cargos devem ser criadas antes da empresa ser criada
Deve seguir a estrutura abaixo:
lista_de_cargos = [Heart.Cargos("Nome do cargo", Salário),] 
'''
cargos = [ 
    Heart.Cargos("Caixa", 1500),
    Heart.Cargos("Gerente", 5000),
    Heart.Cargos("Faxineiro", 1000),
    Heart.Cargos("Vendedor", 2000),
    Heart.Cargos("Diretor", 10000)
]

''' 
Criação da empresa

Deve seguir a estrutura abaixo:
empresa = Heart.Empresa("Nome da empresa", CNPJ, link_fb='ID do link do banco de dados do firebase (exemplo-48483-default-rtdb)', cargos=lista_de_cargos) 
'''
empresa = Heart.Empresa("Projeto Python", 123456789, link_fb='exemplo-48483-default-rtdb', cargos=cargos)


from app.controllers import default  # Importa o arquivo default.py que contém as rotas da aplicação