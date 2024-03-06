from app import app, render_template, empresa, request, criar_funcionario, definir_cargo_funcionario, jsonify 


@app.route('/')
def home():  # Rota para a página inicial
    funcionarios = [funcionario for funcionario in empresa.listar_funcionarios()]
    todos_funcionarios =  jsonify(funcionarios)
    return render_template('index.html', nome=empresa.nome, funcionarios=todos_funcionarios.json)

@app.route('/todos')
def todos():  # Rota para a página com todos os funcionários
    funcionarios = [funcionario for funcionario in empresa.listar_funcionarios()]
    todos_funcionarios =  jsonify(funcionarios)
    return render_template('todos.html', nome=empresa.nome, funcionarios=todos_funcionarios.json)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():  # Rota para a página de cadastro de funcionários
    mensagemP = None
    mensagemN = None
    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        nascimento = request.form['nascimento']
        contratacao = request.form['contratacao']
        sucesso = criar_funcionario(nome, cpf, nascimento, contratacao)
        if sucesso:
            mensagemP = "Funcionário cadastrado com sucesso."
        else:
            mensagemN = "Falha ao cadastrar funcionário."
    return render_template('cadastrar.html', mensagemP=mensagemP, mensagemN=mensagemN, nome=empresa.nome)

@app.route('/buscar', methods=['GET', 'POST'])
def buscar():  # Rota para a página de busca de funcionários
    funcionario = None
    errou = None
    if request.method == 'POST':
        cpf = request.form['cpf']
        try:
            funcionario = empresa.buscar_funcionario(cpf)
        except ValueError as e:
            errou = str(e)
    return render_template('buscar.html', funcionario=funcionario, errou=errou, nome=empresa.nome)

@app.route('/demitir', methods=['GET', 'POST'])
def demitir_funcionario():  # Rota para a página de demissão de funcionários
    mensagemP = None
    mensagemN = None
    if request.method == 'POST':
        cpf = request.form.get('cpf')
        try:
            empresa.demitir_funcionario(cpf)
            mensagemP = "Funcionário demitido com sucesso."
        except ValueError as e:
            mensagemN = str(e)
        # return "Funcionário demitido"
    return render_template('demitir.html', mensagemP=mensagemP, mensagemN=mensagemN, nome=empresa.nome)

@app.route('/definir_cargo', methods=['GET', 'POST'])
def definir_cargo():  # Rota para a página de definição de cargo
    mensagemP = None
    mensagemN = None
    if request.method == 'POST':
        cpf = request.form['cpf']
        cargo = request.form['cargo']
        try:
            definir_cargo_funcionario(cpf, cargo)
            mensagemP = "Cargo definido com sucesso."
        except ValueError as e:
            mensagemN = str(e)
    return render_template('definir_cargo.html', mensagemP=mensagemP, mensagemN=mensagemN, nome=empresa.nome)