from flask import Flask, render_template, redirect, url_for, request, make_response
import pdfkit
import controler

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
        self.registroProfissional =  registroProfissional
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
    if request.method == "POST":  
        if request.form["radio"] == '0': #cliente
            nome = request.form["nome"]
            data_de_nascimento = request.form["nascimento"]
            cpf = controler.limpa_cpf(request.form["cpf"])
            telefone = controler.limpa_telefone(request.form["telefone"])
            email = request.form["email"]
            senha = request.form["senha"]
            cep=request.form["cep"]
            endereco = request.form["endereco"]
            numero = request.form["numero"]
            complemento = request.form["complemento"]
            cidade = request.form["cidade"]
            estado = request.form["estado"]
            if controler.verifica_idade(data_de_nascimento)==False:
                nome_responsavel = '-'
                cpf_responsavel = '-'
            else:
                nome_responsavel = request.form["nomeRes"]
                cpf_responsavel = request.form["cpfRes"]

            controler.cadastra_cliente(nome, data_de_nascimento, cpf, telefone, email, senha, cep, endereco, numero, complemento, cidade, estado, nome_responsavel, cpf_responsavel)               
            return redirect("http://127.0.0.1:5000/")

        if request.form["radio"] == '1': #profissional
            nome = request.form["nome"]
            cpf = controler.limpa_cpf(request.form["cpf"])
            profissao = request.form["profissao"]
            registro_profissional = request.form["regProf"]
            telefone = controler.limpa_telefone(request.form["telefone"])
            data_de_nascimento = request.form["nascimento"]
            email = request.form["email"]
            senha = request.form["senha"]
            cep=request.form["cep"]
            endereco = request.form["endereco"]
            numero = request.form["numero"]
            complemento = request.form["complemento"]
            cidade = request.form["cidade"]
            estado = request.form["estado"]
            controler.cadastra_profissional(nome, cpf, profissao, registro_profissional, telefone, data_de_nascimento, email, senha, cep, endereco, numero, complemento, cidade, estado)
            return redirect("http://127.0.0.1:5000/")

    return render_template('create.html')


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method =='POST':
        cpf_inserido = controler.limpa_cpf(request.form["cpf"])
        senha_inserida = request.form["senha"]

#### A mudança pra pessoa que tem conta cliente e profissional vai ser aqui. Algo do tipo
# if cpf in clientes and cpf in profissionais:
# redirect pra uma pagina "logged", intermediária
# nessa página a pessoa decide em qual conta vai entrar
        if controler.verifica_cpf(cpf_inserido, "clientes"): # ta na bd
            if senha_inserida==controler.cpf_senha(cpf_inserido, "clientes"):
                id_cliente = controler.select("id_cliente","clientes", "cpf="+cpf_inserido)[0][0]
                return redirect(url_for('loggedCliente', id_cliente=id_cliente))
            else:
                error = "Senha incorreta!"

        elif controler.verifica_cpf(cpf_inserido, "profissionais"): # ta na bd
            if senha_inserida==controler.cpf_senha(cpf_inserido, "profissionais"):
                id_profissional = controler.select("id_profissional","profissionais", "cpf="+cpf_inserido)[0][0]
                return redirect(url_for('loggedProfissional', id_profissional=id_profissional))
            else:
                error = "Senha incorreta!"

        else:
            error = "Usuário não cadastrado"

    return render_template('login.html', error=error)


@app.route('/loggedProfissional/<id_profissional>')
def loggedProfissional(id_profissional):
    nome = controler.select("nome","profissionais", "id_profissional="+str(id_profissional))[0][0]
    return render_template("loggedProfissional.html", profissional=nome)


@app.route('/loggedCliente/<id_cliente>')
def loggedCliente(id_cliente):
    nome = controler.select("nome","clientes", "id_cliente="+str(id_cliente))[0][0]
    return render_template("loggedCliente.html", cliente=nome)


if __name__ == '__main__':
    app.run(debug=True)
