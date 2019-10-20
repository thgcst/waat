from flask import Flask, render_template, redirect, url_for, request, make_response
import pdfkit
import controler

app = Flask(__name__)
"""
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
    def __init__(self, nome, cpf, senha, profissao, regProf):
        super().__init__(nome, cpf, senha)                              #Usando o fato de ser subclasse e herdando metodos e atributos da classe mãe
        self.regProf =  regProf
        self.profissao = profissao
        self.regProf =  regProf
        self.cep = cep

    def set_profissao(self, profissao):
        self.profissao = profissao

    def set_regProf(self, regProf):
        self.regProf =  regProf

    def get_profissional(self):
        return (self.profissao)

    def get_regProf(self):
        return(self.regProf)


class Cliente(Usuário):                                              #Criando Clase profissional que é subclasse de Usuário

    def __init__(self, nome, cpf, senha, precoConsulta, nomeRes, cpfRes, enderecoResponsavel, frequencia, diaDaSemana, horario):

        super().__init__(nome, cpf, senha)                           #Usando o fato de ser subclasse e herdando metodos e atributos da classe mãe
        self.precoConsulta =  precoConsulta
        self.nomeRes = nomeRes
        self.cpfRes = cpfRes
        self.enderecoResponsavel = enderecoResponsavel
        self.diaDaSemana = diaDaSemana
        self.horario = horario

    def set_precoConsulta(self,precoConsulta):
        self.precoConsulta = precoConsulta

    def set_nomeRes(self, nomeRes ):
        self.nomeRes = nomeRes

    def set_cpfRes(self, cpfRes ):
        self.cpfRes = cpfRes

    def set_enderecoResponsavel(self, enderecoResponsavel ):
        self.enderecoResponsavel = enderecoResponsavel

    def set_diaDaSemana(self, diaDaSemana ):
        self.diaDaSemana = diaDaSemana

    def set_horario(self, horario ):
        self.horario = horario

    def get_precoConsulta(self):
        return(self.precoConsulta)

    def get_nomeRes(self):
        return(self.nomeRes)

    def get_cpfRes(self):
        return(self.cpfRes)

    def get_enderecoResponsavel(self):
        return(self.enderecoResponsavel)

    def get_diaDaSemana(self):
        return(self.diaDaSemana)

    def get_horario(self):
        return(self.horario)

    def get_cliente(self):
        return str(self.nome) + "," + str(self.cpf) + "," + str(self.nomeRes) + "," + str(self.cpfRes) + "," + str(self.senha) + "\n"

clientes = []
clienteAtual = 0
"""
class Cliente:

    def __init__(self, id):
        self.id = str(id)
        self.nome = controler.select('nome', 'clientes', 'id_cliente='+self.id)[0][0]
        self.cpf = controler.select('cpf', 'clientes', 'id_cliente='+self.id)[0][0]
        self.senha = controler.select('senha', 'clientes', 'id_cliente='+self.id)[0][0]
        self.nomeRes = controler.select('nome_responsavel', 'clientes', 'id_cliente='+self.id)[0][0]
        self.cpfRes = controler.select('cpf_responsavel', 'clientes', 'id_cliente='+self.id)[0][0]
        self.endereco = controler.select('endereco', 'clientes', 'id_cliente='+self.id)[0][0]

    def set_nome(self, nome):
        controler.update({'nome':nome}, 'clientes', 'id_cliente='+self.id)
        self.nome = controler.select('nome', 'clientes', 'id_cliente='+self.id)[0][0]
        
    def set_cpf(self, cpf):
        controler.update({'cpf':cpf}, 'clientes', 'id_cliente='+self.id)
        self.nome = controler.select('cpf', 'clientes', 'id_cliente='+self.id)[0][0]
        
    def set_senha(self, senha):
        controler.update({'senha':senha}, 'clientes', 'id_cliente='+self.id)
        self.nome = controler.select('senha', 'clientes', 'id_cliente='+self.id)[0][0]

@app.route('/<nomeProfissional>/<regProf>/<profissao>/<nome>/<cpf>/<precoConsulta>/<email>/<enderecoComercial>/<telefone>/<cep>')
def pdf_template1(nomeProfissional, regProf, profissao, nome, cpf, precoConsulta, email, enderecoComercial, telefone, cep):
    rendered = render_template('pdf_template18+.html', nomeProfissional = nomeProfissional, regProf = regProf, profissao = profissao, nome = nome, cpf = cpf, precoConsulta = precoConsulta, email=email, enderecoComercial = enderecoComercial, telefone = telefone, cep = cep)
    pdf = pdfkit.from_string(rendered, False)

    response =  make_response(pdf)
    response.headers['Content-Type'] =  'applocation/pdf'
    response.headers['Content-Disposition'] =   'inline; filename = recibo.pdf'

    return response

@app.route('/<nomeProfissional>/<regProf>/<profissao>/<nome>/<cpfRes>/<nomeRes>/<precoConsulta>/<email>/<enderecoComercial>/<telefone>/<cep>')
def pdf_template2(nomeProfissional, regProf, profissao, nome, cpfRes, nomeRes, precoConsulta, email, enderecoComercial, telefone, cep):
    rendered = render_template('pdf_template18-.html', nomeProfissional = nomeProfissional, regProf = regProf, profissao = profissao, nome = nome, cpfRes = cpfRes, nomeRes = nomeRes, precoConsulta = precoConsulta, email=email, enderecoComercial = enderecoComercial, telefone = telefone, cep = cep)
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
            if nome=='' or data_de_nascimento=='' or cpf=='' or telefone=='' or email=='' or senha=='' or cep=='' or endereco=='' or numero=='' or complemento=='' or cidade=='' or estado=='':
                error = 'Preencha todos os campos!'
            elif controler.verifica_cpf(cpf, 'clientes'):
               error = 'Usuário Cadastrado!'
            else:
                if controler.verifica_idade(data_de_nascimento)==False:
                    nome_responsavel = '-'
                    cpf_responsavel = '-'
                    controler.cadastra_cliente(nome, data_de_nascimento, cpf, telefone, email, senha, cep, endereco, numero, complemento, cidade, estado, nome_responsavel, cpf_responsavel)
                    return redirect("http://127.0.0.1:5000/")
                else:
                    nome_responsavel = request.form["nomeRes"]
                    cpf_responsavel = request.form["cpfRes"]
                    if nome_responsavel or cpf_responsavel =='':
                        error = 'Preencha todos os campos!'
                    else:
                        controler.cadastra_cliente(nome, data_de_nascimento, cpf, telefone, email, senha, cep, endereco, numero, complemento, cidade, estado, nome_responsavel, cpf_responsavel)
                        return redirect("http://127.0.0.1:5000/")

        if request.form["radio"] == '1': #profissional
            nome = request.form["nomePro"]
            cpf = controler.limpa_cpf(request.form["cpfPro"])
            profissao = request.form["profissaoPro"]
            registro_profissional = request.form["regProf"]
            telefone = controler.limpa_telefone(request.form["telefonePro"])
            data_de_nascimento = request.form["nascimentoPro"]
            email = request.form["emailPro"]
            senha = request.form["senhaPro"]
            cep=request.form["cepPro"]
            endereco = request.form["enderecoPro"]
            numero = request.form["numeroPro"]
            complemento = request.form["complementoPro"]
            cidade = request.form["cidadePro"]
            estado = request.form["estadoPro"]

            if nome=='' or cpf=='' or profissao=='' or registro_profissional=='' or telefone=='' or data_de_nascimento=='' or email=='' or senha=='' or cep=='' or endereco=='' or numero=='' or complemento=='' or cidade=='' or estado=='':
                error = 'Preencha todos os campos!'
            else:
                if controler.verifica_cpf(cpf, 'profissionais'):
                    error = 'Usuário Cadastrado!'
                else:
                    controler.cadastra_profissional(nome, cpf, profissao, registro_profissional, telefone, data_de_nascimento, email, senha, cep, endereco, numero, complemento, cidade, estado)
                    return redirect("http://127.0.0.1:5000/")
    return render_template('create.html', error=error)


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
    user = Cliente(id_cliente)
    return render_template("loggedCliente.html", cliente=user.nome)

@app.route('/sobreNos', methods=['GET', 'POST'])
def sobreNos():
    error = None
    if request.method =='POST':
        return redirect(url_for('cadastro'))

    return render_template('sobreNos.html', error=error)


if __name__ == '__main__':
    app.run(debug=True)
