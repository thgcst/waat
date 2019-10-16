from flask import Flask, render_template, redirect, url_for, request, make_response
#import pdfkit, controler

app = Flask(__name__)

#Criando super classe usuario, que possui os atributos que sao comuns ao profissional ou cliente que vai usar a plataforma
class Usuário():
    def __init__(self, nome, cpf, senha ):
        self.nome = nome
        self.cpf = cpf
        self.senha = senha

    def set_nome(self, nome):
        self.nome = nome

    def set_cpf(self, cpf):
        self.cpf = cpf

    def set_senha(self, senha):
        self.senha =  senha

    def get_nome(self):
        return (self.nome)

    def get_cpf(self):
        return (self.cpf)

    def get_senha(self):
        return (self.senha)

class Profissional(Usuário):
    def __init__(self, nome, cpf, senha, profissao, registroProfissional):
        super().__init__(nome, cpf, senha)                              #Usando o fato de ser subclasse e herdando metodos e atributos da classe mãe
        self.resgistroProfissional =  resgistroProfissional
        self.profissao = profissao
        self.registroProfissional =  registroProfissional

    def set_profissao(self, profissao):
        self.profissao = profissao

    def set_registroProfissional(self, registroProfissional):
        self.registroProfissional =  registroProfissional

    def get_profissional(self):
        return (self.profissao)

    def get_registroProfissional(self):
        return(self.registroProfissional)


class Cliente(Usuário):                                              #Criando Clase profissional que é subclasse de Usuário

    def __init__(self, nome, cpf, senha, precoConsulta, nomeResponsavel, cpfResponsavel, enderecoResponsavel, frequencia, diaDaSemana, horario):

        super().__init__(nome, cpf, senha)                           #Usando o fato de ser subclasse e herdando metodos e atributos da classe mãe
        self.precoConsulta =  precoConsulta
        self.nomeResponsavel = nomeResponsavel
        self.cpfResponsavel = cpfResponsavel
        self.enderecoResponsavel = enderecoResponsavel
        self.diaDaSemana = diaDaSemana
        self.horario = horario

    def set_precoConsulta(self,precoConsulta):
        self.precoConsulta = precoConsulta

    def set_nomeResponsavel(self, nomeResponsavel ):
        self.nomeResponsavel = nomeResponsavel

    def set_cpfResponsavel(self, cpfResponsavel ):
        self.cpfResponsavel = cpfResponsavel

    def set_enderecoResponsavel(self, enderecoResponsavel ):
        self.enderecoResponsavel = enderecoResponsavel

    def set_diaDaSemana(self, diaDaSemana ):
        self.diaDaSemana = diaDaSemana

    def set_horario(self, horario ):
        self.horario = horario

    def get_precoConsulta(self):
        return(self.precoConsulta)

    def get_nomeResponsavel(self):
        return(self.nomeResponsavel)

    def get_cpfResponsavel(self):
        return(self.cpfResponsavel)

    def get_enderecoResponsavel(self):
        return(self.enderecoResponsavel)

    def get_diaDaSemana(self):
        return(self.diaDaSemana)

    def get_horario(self):
        return(self.horario)

    def get_cliente(self):
        return str(self.nome) + "," + str(self.cpf) + "," + str(self.nomeResponsavel) + "," + str(self.cpfResponsavel) + "," + str(self.senha) + "\n"

clientes = []
clienteAtual = 0

@app.route('/<nomeProfissional>/<registroProfissional>/<profissao>/<nome>/<cpf>/<precoConsulta>/<email>/<enderecoComercial>/<telefone>')
def pdf_template(nomeProfissional, registroProfissional, profissao, nome, cpf, precoConsulta, email, enderecoComercial, telefone):
    rendered = render_template('pdf_template18+.html', nomeProfissional = nomeProfissional, registroProfissional = registroProfissional, profissao = profissao, nome = nome, cpf = cpf, precoConsulta = precoConsulta, email=email, enderecoComercial= enderecoComercial, telefone=telefone)
    pdf = pdfkit.from_string(rendered, False)

    response =  make_response(pdf)
    response.headers['Content-Type'] =  'applocation/pdf'
    response.headers['Content-Disposition'] =   'inline; filename = recibo.pdf'

    return response



@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    error = None
    if request.method == "POST":  #cliente
        if request.form["nome"] == "" or request.form["cpf"] == "" or request.form["nascimento"] == "" or request.form["tel"] == "" or request.form["endereco"] or request.form["senha"] == "" or request.form["cpfResponsavel"] == "" or request.form["nomeResponsavel"] == "":
            error = "Preencha todos os campos!"
        else:
            nome = request.form["nome"]
            data_de_nascimento = request.form["nascimento"]
            cpf = request.form["cpf"]
            tel = request.form["tel"]
            endereco = request.form["endereco"]
            email = request.form["email"]
            senha = request.form["senha"]
            nome_responsavel = request.form["nomeResponsavel"]
            cpf_responsavel = request.form["cpfResponsavel"]
            controler.cadastra_cliente(nome, data_de_nascimento, cpf, tel, endereco, email, senha, cpf_resposavel, nome_resposavel)                
            error = None
    return render_template('create.html' , error=error)


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method =='POST':
        cpf_inserido = request.form["cpf"]
        senha_inserida = request.form["senha"]
        if controler.verifica_cpf(cpf_inserido): # ta na bd
            if senha_inserida==controler.cpf_senha(cpf_inserido):
                id_cliente = controler.select("id_cliente","clientes", "cpf="+cpf_inserido)[0][0]
                return redirect(url_for('logged', id_cliente=id_cliente))
            else:
                error = "Senha incorreta!"
        else:
            error = "Usuário não cadastrado"
    return render_template('login.html', error=error)


@app.route('/logged/<id_cliente>')
def logged(id_cliente):
    nome = controler.select("nome","clientes", "id_cliente="+str(id_cliente))[0][0]
    return render_template("loggedCliente.html", cliente=nome)


if __name__ == '__main__':
    app.run(debug=True)
