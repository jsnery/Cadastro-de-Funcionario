from dataclasses import dataclass, field
import requests, json


@dataclass
class Funcionarios:
    Nome: str = field(kw_only=True)
    Nascimento: str = field(kw_only=True)
    CPF: str = field(kw_only=True)
    Admissao: str = field(kw_only=True)
    Cargo: str = field(default=None, repr=False)
    Salario: float = field(default=None, repr=False)

    @property
    def _dados_funcionario(self) -> dict:
        return {
            "Nome": self.Nome,
            "Nascimento": self.Nascimento,
            "CPF": self.CPF,
            "Admissao": self.Admissao,
            "Cargo": self.Cargo,
            "Salario": self.Salario
        }

@dataclass        
class Cargos:  # Classe para criar cargos
    nome: str
    salario: int

@dataclass
class Empresa: # Classe para criar uma empresa
    nome: str = field(kw_only=True)
    cnpj: int = 1
    link_fb: str = field(default='', repr=False, kw_only=True)
    cargos: list = field(default_factory=list, repr=False, kw_only=True)
    funcionarios: dict = field(default_factory=dict, repr=False, init=False)

    def __post_init__(self):
        self.__link_fb = f"https://{self.link_fb}.firebaseio.com/Funcionarios/.json"
        self.funcionarios = requests.get(self.__link_fb).json()

    '''Valida o CPF do funcionário'''
    @staticmethod
    def __validar_cpf(funcionario):
        # Remover caracteres não numéricos
        try:
            cpf = ''.join(c for c in f'{funcionario.CPF}' if c.isdigit())
        except:
            cpf = ''.join(c for c in f'{funcionario}' if c.isdigit())

        # Verificar se o CPF tem 11 dígitos
        if len(cpf) != 11:
            return False

        # Verificar se o CPF tem todos os dígitos iguais, que é inválido
        if cpf == cpf[0] * 11:
            return False

        # Calcular o primeiro dígito de verificação
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        d1 = 11 - (soma % 11)
        if d1 >= 10:
            d1 = 0

        # Calcular o segundo dígito de verificação
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        d2 = 11 - (soma % 11)
        if d2 >= 10:
            d2 = 0

        # Verificar se os dígitos de verificação são corretos
        return cpf[-2:] == f"{d1}{d2}"

    '''Remove a pontuação do CPF'''
    @staticmethod
    def remover_ponturacao_do_cpf(cpf):
        return ''.join(c for c in f'{cpf}' if c.isdigit())
       
    '''Atualiza o banco de dados do firebase com os dados dos funcionários'''
    @property
    def __atualizar_db(self):
        try:
            requests.put(self.__link_fb, data=json.dumps(self.funcionarios))
        except requests.exceptions.RequestException as e:
            print(f"Erro ao atualizar o banco de dados: {e}")
            raise ValueError("Banco de dados não encontrado")

    '''Lista todos os funcionários da empresa e retorna um dicionário com os dados dos funcionários'''
    @property
    def listar_funcionarios(self):
        for cpf in self.funcionarios:
            yield  self.funcionarios[cpf]

    '''Contrata um funcionário e adiciona ao banco de dados do firebase'''            
    def contratar_funcionario(self, funcionario):
        if not self.__validar_cpf(funcionario):
            raise ValueError("CPF inválido")
        cpf_sem_pontuacao = self.remover_ponturacao_do_cpf(funcionario.CPF)
        self.funcionarios.update({cpf_sem_pontuacao: funcionario._dados_funcionario})   
        self.__atualizar_db  

    '''Demitir um funcionário e atualiza o banco de dados do firebase'''
    def demitir_funcionario(self, cpf):
        if not self.__validar_cpf(cpf):
            raise ValueError("CPF inválido")
        cpf_sem_pontuacao = self.remover_ponturacao_do_cpf(cpf)
        if cpf_sem_pontuacao not in self.funcionarios:
            raise ValueError("Funcionário não encontrado")
        self.funcionarios.pop(cpf_sem_pontuacao, None)
        self.__atualizar_db

    '''Define o cargo e salário de um funcionário e atualiza o banco de dados do firebase'''
    def definir_cargo_funcionario(self, cpf: int|str, cargo):
        cargo = int(cargo)
        if cargo > len(self.cargos) or cargo < 0:
            raise ValueError("Cargo inválido")
        if not self.__validar_cpf(cpf):
            raise ValueError("CPF inválido")
        cpf_sem_pontuacao = self.remover_ponturacao_do_cpf(cpf)
        if cpf_sem_pontuacao not in self.funcionarios:
            raise ValueError("Funcionário não encontrado")
        self.funcionarios[cpf_sem_pontuacao].update({
            "Cargo": self.cargos[cargo].nome,
            "Salario": self.cargos[cargo].salario
        })
        self.__atualizar_db

    '''Busca um funcionário pelo CPF e retorna um objeto Funcionarios'''
    def buscar_funcionario(self, cpf):
        if not self.__validar_cpf(cpf):
            raise ValueError("CPF inválido")
        cpf_sem_pontuacao = self.remover_ponturacao_do_cpf(cpf)
        if cpf_sem_pontuacao not in self.funcionarios:
            raise ValueError("Funcionário não encontrado")
        return self.funcionarios[cpf_sem_pontuacao]