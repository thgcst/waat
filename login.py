from flask import Flask, render_template, redirect, url_for, request, make_response
import pdfkit

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
    def __init__(self, nome, cpf, senha, profissao, registoProfissional):
        super().__init__(nome, cpf, senha)                              #Usando o fato de ser subclasse e herdando metodos e atributos da classe mãe
        self.profissao = profissao
        self.registoProfissional =  registoProfissional

    def set_profissao(self, profissao):
        self.profissao = profissao

    def set_registroProfissional(self, registoProfissional):
        self.registoProfissional =  registoProfissional

    def get_profissional(self):
        return (self.profissao)

    def get_registroProfissional(self):
        return(self.registoProfissional)


class Cliente(Usuário):                                              #Criando Clase profissional que é subclasse de Usuário

    def __init__(self, nome, cpf, senha, precoConsulta, nomeResponsavel, cpfResponsavel, enderecoResponsavel, frequencia, diaDaSemana, horario):

        super().__init__(nome, cpf, senha)                           #Usando o fato de ser subclasse e herdando metodos e atributos da classe mãe
        self.precoConsulta =  precoConsulta
        self.nomeResponsavel = nomeResponsavel
        self.cpfResponsavel = cpfResponsavel
        self.enderecoResponsavel = enderecoResponsavel
        self.frequencia =  frequencia
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

    def set_frequencia(self, frequencia ):
        self.frequencia =  frequencia

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

    def get_frequencia(self):
        return(self.frequencia)

    def get_diaDaSemana(self):
        return(self.diaDaSemana)

    def get_horario(self):
        return(self.horario)

    def get_cliente(self):
        return str(self.nome) + "," + str(self.cpf) + "," + str(self.nomeResponsavel) + "," + str(self.cpfResponsavel) + "," + str(self.senha) + "\n"



clientes = []
clienteAtual = 0


@app.route('/<nomePofissional>/<registoProfissional>/<nomeResponsavel>/<cpfResponsavel>/<precoConsulta>')
def pdf_template(nomePofissional, registoProfissional, nomeResponsavel, cpfResponsavel, precoConsulta):
    rendered = render_template('pdf_template.html', nomePofissional = nomePofissional, registoProfissional = registoProfissional, nomeResponsavel = nomeResponsavel, cpfResponsavel = cpfResponsavel, precoConsulta = precoConsulta)
    pdf = pdfkit.from_string(rendered, False)

    response =  make_response(pdf)
    response.headers['Content-Type'] =  'applocation/pdf'
    response.headers['Content-Disposition'] =   'inline; filename = recibo.pdf'

    return response



@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    error = None
    if request.method == "POST":
        if request.form["nome"] == "" or request.form["cpfResponsavel"] == "" or request.form["cpf"] == "" or request.form["nome"] == "" or request.form["senha"] == "":
            error = "Preencha todos os campos!"
        else:
            cliente1 = Cliente(request.form["nome"], str(request.form["cpf"]), str(request.form["senha"]), 0, str(request.form["nomeResponsavel"]), request.form["cpfResponsavel"], 0, 0, 0, 0)
            arq = open('lista.txt', 'a')
            arq.writelines(cliente1.get_cliente())
            arq.close()
            error = None

    return render_template('create.html' , error=error)



@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method =='POST':

        arq = open('lista.txt', 'r')
        texto = arq.readlines()
        for i in range(0,len(texto)) :
            clientes.append(texto[i].split(","))
        arq.close()

        for i in range(0,len(clientes)):
            if clientes[i][0] == request.form["cpf"]:
                if clientes[i][1] == request.form["senha"]:
                    clienteAtual = i
                    error = str(i)
                    return redirect(url_for('loggedPaciente'))
                    break
                else:
                    error = "Senha incorreta!"
                    break
            if i == len(clientes)-1:
                error = "Usuário não cadastrado"


        # error = 'O usuário "' + request.form['cpf'] + '" não está cadastrado!'

    return render_template('login.html', error=error)


@app.route('/logged')
def logged():
    return render_template("loggedPaciente.html", nome=joão)



if __name__ == '__main__':
    app.run(debug=True)
