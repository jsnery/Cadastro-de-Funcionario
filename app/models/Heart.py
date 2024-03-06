import requests, json


class Funcionarios:  # Classe para criar funcionários

    '''Cria um funcionário com um nome, data de nascimento, CPF e data de contratação'''
    def __init__(self, nome: str, nascimento: str, cpf: str, data_de_contratacao: str):
        self.nome = nome
        self.nascimento = nascimento
        self.cpf = cpf
        self.data_de_contratacao = data_de_contratacao
        self.cargo = None
        self.salario = None

    def __str__(self):
        return f"Nome: {self.nome}\nCargo: {self.cargo}\nContratado: {self.data_de_contratacao}"
    
    '''Retorna um dicionário com os dados do funcionário para ser adicionado ao banco de dados do firebase'''
    def _dados_funcionario(self) -> dict:
        return {
            "Nome": self.nome,
            "Nascimento": self.nascimento,
            "CPF": self.cpf,
            "Admissao": self.data_de_contratacao,
            "Cargo": self.cargo,
            "Salario": self.salario
            }   
    
class Empresa: # Classe para criar uma empresa

    '''Cria uma empresa com um nome e CNPJ e 
       verifica se já existe um banco de dados 
       no firebase, caso não exista, cria um 
       novo banco de dados com o nome da empresa'''
    def __init__(self, nome: str, cnpj: int, link_fb: str = "", cargos: list = []):
        self.nome = nome
        self.cnpj = cnpj
        self.cargos = cargos  # Lista de cargos da empresa
        self.__link_fb = f"https://{link_fb}.firebaseio.com/Funcionarios/.json"  # Link do banco de dados do firebase
        self.funcionarios = requests.get(self.__link_fb).json()

    '''Valida o CPF do funcionário'''
    @staticmethod
    def __validar_cpf(funcionario):
        # Remover caracteres não numéricos
        try:
            cpf = ''.join(c for c in f'{funcionario.cpf}' if c.isdigit())
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
    def __atualizar_db(self):
        try:
            requests.put(self.__link_fb, data=json.dumps(self.funcionarios))
        except requests.exceptions.RequestException as e:
            print(f"Erro ao atualizar o banco de dados: {e}")
            raise ValueError("Banco de dados não encontrado")

    '''Contrata um funcionário e adiciona ao banco de dados do firebase'''            
    def contratar_funcionario(self, funcionario):
        if not self.__validar_cpf(funcionario):
            raise ValueError("CPF inválido")
        cpf_sem_pontuacao = self.remover_ponturacao_do_cpf(funcionario.cpf)
        self.funcionarios.update({cpf_sem_pontuacao: funcionario._dados_funcionario()})   
        self.__atualizar_db()    

    '''Demitir um funcionário e atualiza o banco de dados do firebase'''
    def demitir_funcionario(self, cpf):
        if not self.__validar_cpf(cpf):
            raise ValueError("CPF inválido")
        cpf_sem_pontuacao = self.remover_ponturacao_do_cpf(cpf)
        if cpf_sem_pontuacao not in self.funcionarios:
            raise ValueError("Funcionário não encontrado")
        self.funcionarios.pop(cpf_sem_pontuacao, None)
        self.__atualizar_db()

    '''Define o cargo e salário de um funcionário e atualiza o banco de dados do firebase'''
    def definir_cargo_funcionario(self, funcionario, cargo):
        cargo = int(cargo)
        if cargo > len(self.cargos) or cargo < 0:
            raise ValueError("Cargo inválido")
        if not self.__validar_cpf(funcionario):
            raise ValueError("CPF inválido")
        cpf_sem_pontuacao = self.remover_ponturacao_do_cpf(funcionario)
        if cpf_sem_pontuacao not in self.funcionarios:
            raise ValueError("Funcionário não encontrado")
        self.funcionarios[cpf_sem_pontuacao].update({
            "Cargo": self.cargos[cargo].nome,
            "Salario": self.cargos[cargo].salario
        })
        self.__atualizar_db()

    '''Busca um funcionário pelo CPF e retorna um objeto Funcionarios'''
    def buscar_funcionario(self, cpf):
        if not self.__validar_cpf(cpf):
            raise ValueError("CPF inválido")
        cpf_sem_pontuacao = self.remover_ponturacao_do_cpf(cpf)
        if cpf_sem_pontuacao not in self.funcionarios:
            raise ValueError("Funcionário não encontrado")
        return self.funcionarios[cpf_sem_pontuacao]

    '''Lista todos os funcionários da empresa e retorna um dicionário com os dados dos funcionários'''
    def listar_funcionarios(self):
        for cpf in self.funcionarios:
            yield  self.funcionarios[cpf]
        # return self.funcionarios
            
class Cargos:  # Classe para criar cargos
    def __init__(self, nome, salario):
        self.nome = nome
        self.salario = salario

    def __str__(self):
        return f"Cargo: {self.nome}\nSalario: {self.salario}"


# if __name__ == "__main__":  # Teste das classes

#     cargos = [Cargos("Caixa", 1500), Cargos("Gerente", 5000), Cargos("Faxineiro", 1000), Cargos("Vendedor", 2000), Cargos("Diretor", 10000)]
#     empresa = Empresa("Wallmart", 123456789, link_fb='exemplo-48483-default-rtdb', cargos=cargos)
   

#     Jane = Funcionarios("John Doe", "14/02/2001", '974.016.460-99', '04/03/2024')
#     John = Funcionarios("Jane Doe", "28/12/1999", '958.392.500-40', '04/03/2024')

    
#     empresa.contratar_funcionario(sara)
#     empresa.contratar_funcionario(matheus)
#     # empresa.definir_cargo_funcionario(Jane, 1)
#     # empresa.definir_cargo_funcionario(John, 0)
#     # empresa.demitir_funcionario('958.392.500-40')
#     # print(empresa.buscar_funcionario('974.016.460-99'))

#     for i in empresa.listar_funcionarios():
#         print(i['Nome'].split()[0])