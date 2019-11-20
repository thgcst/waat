from flask import Flask, render_template, redirect, url_for, request, make_response, session, g
import pdfkit
import controler
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, datetime
import secrets
import uuid

app = Flask(__name__)

app.secret_key = "PipocaSalgada"

class Usuario():

    def __init__(self, id):
        self.id = str(id)
        
        dados = controler.select_CursorDict('*', 'usuarios', 'id='+self.id)[0]
        self.nome = dados['nome']
        self.data_de_nascimento = dados['data_de_nascimento']
        self.cpf = dados['cpf']
        self.telefone = dados['telefone']
        self.email = dados['email']
        self.senha = dados['senha']
        self.tipo = dados['tipo']

    def up_nome(self, nome):
        controler.update({'nome':nome}, 'clientes', 'id='+self.id)
        self.nome = controler.select('nome', 'clientes', 'id='+self.id)[0][0]

    def up_senha(self, senha):
        controler.update({'senha':senha}, 'clientes', 'id='+self.id)
        self.senha = controler.select('senha', 'clientes', 'id='+self.id)[0][0]


class Profissional(Usuario):
    def __init__(self,id):
        super().__init__(id)                              #Usando o fato de ser subclasse e herdando metodos e atributos da classe mãe
        dados = controler.select_CursorDict('*', 'profissionais', 'id_profissional='+self.id)[0]
        self.profissao = dados['profissao']
        self.registro_profissional = dados['registro_profissional']
        self.telefone_comercial = dados['telefone_comercial']
        self.cep = dados['cep']
        self.endereco = dados['endereco']
        self.numero = dados['numero']
        self.complemento = dados['complemento']
        self.cidade = dados['cidade']
        self.estado = dados['estado']


class Cliente(Usuario):                                              #Criando Clase profissional que é subclasse de Usuário

    def __init__(self,id):
        super().__init__(id)                           #Usando o fato de ser subclasse e herdando metodos e atributos da classe mãe
        dados = controler.select_CursorDict('*', 'clientes', 'id_cliente='+self.id)[0]
        self.cep = dados['cep']
        self.endereco = dados['endereco']
        self.numero = dados['numero']
        self.complemento = dados['complemento']
        self.cidade = dados['cidade']
        self.estado = dados['estado']
        self.nome_responsavel = dados['nome_responsavel']
        self.cpf_responsavel = dados['cpf_responsavel']

# tipo 0 - semicadastro  1 - cliente  2 - profissional  3 - cliprof
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    error = None
    if request.method == "POST": #cliente
        if request.form["radio"] == '0':
            nome = request.form["nome"]
            data_de_nascimento = request.form["nascimento"]
            cpf = request.form["cpf"]
            telefone = controler.limpa_telefone(request.form["telefone"])
            email = request.form["email"]
            senha = request.form["senha"]
            cep=request.form["cep"]
            endereco = request.form["endereco"]
            numero = request.form["numero"]
            if request.form["complemento"]=="":
                complemento = "-"
            else:
                complemento = request.form["complemento"]
            cidade = request.form["cidade"]
            estado = request.form["estado"]

            if nome=='' or data_de_nascimento=='' or cpf=='' or telefone=='' or email=='' or senha=='' or cep=='' or endereco=='' or numero=='' or cidade=='' or estado=='':
                error = 'Preencha todos os campos!'
            elif cpf == "CPF Inválido" or len(cpf) != 14:
                error = 'Verifique seu CPF!'
            elif endereco =="CEP não encontrado":
                error = 'Verifique seu CEP!'
            elif controler.verifica_email(email,'usuarios'):
                error = 'Ops! Email já cadastrado.'
            elif len(data_de_nascimento) != 10 or controler.valida_data(data_de_nascimento) or controler.verifica_idade(data_de_nascimento) == "erro":
                error = 'Data de nascimento inválida!'
            else:
                cpf = controler.limpa_cpf(request.form["cpf"])
                if controler.verifica_cpf(cpf, 'usuarios'): #verificar o tipo -> se for 0 -> apenas update
                    tipo = controler.cpf_tipo(cpf,"usuarios")
                    if tipo == 0:
                        pass
                    else: 
                        error = "Este CPF já está cadastrado."

                else:
                    hashed_password = generate_password_hash(senha)
                    if controler.verifica_idade(data_de_nascimento)==False: #maior de idade
                        nome_responsavel = '-'
                        cpf_responsavel = '-'
                        tipo=1
                        controler.cadastra_usuario(cpf, nome, email, telefone, controler.converte_data(data_de_nascimento), hashed_password, tipo)
                        id_cliente = controler.select("id", "usuarios", "cpf="+str(cpf))[0][0]
                        controler.cadastra_cliente(id_cliente,cep,endereco,numero,complemento,cidade,estado, nome_responsavel, cpf_responsavel)
                        return redirect(url_for('login'))
                    
                    else: #menor de idade
                        nome_responsavel = request.form["nomeRes"]
                        cpf_responsavel = request.form["cpfRes"]
                        if nome_responsavel=='' or cpf_responsavel =='':
                            error = 'Preencha todos os campos'
                        elif cpf_responsavel == "CPF Inválido" or len(cpf_responsavel) != 14:
                            error = "Verifique o CPF do responsável"
                        else:
                            tipo=1
                            controler.cadastra_usuario(cpf, nome, email, telefone, controler.converte_data(data_de_nascimento), hashed_password, tipo)
                            id_cliente = controler.select("id", "usuarios", "cpf="+str(cpf))[0][0]
                            controler.cadastra_cliente(id_cliente,cep,endereco,numero,complemento,cidade,estado, nome_responsavel, cpf_responsavel)
                            return redirect(url_for('login'))

        if request.form["radio"] == '1': #profissional
            nome = request.form["nomePro"]
            cpf = request.form["cpfPro"]
            profissao = request.form["profissaoPro"]
            registro_profissional = request.form["regProf"]
            telefone = controler.limpa_telefone(request.form["telefonePro"])
            data_de_nascimento = request.form["nascimentoPro"]
            email = request.form["emailPro"]
            senha = request.form["senhaPro"]
            cep=request.form["cepPro"]
            endereco = request.form["enderecoPro"]
            numero = request.form["numeroPro"]
            if request.form["complemento"]=="":
                complemento = "-"
            else:
                complemento = request.form["complemento"]
            cidade = request.form["cidadePro"]
            estado = request.form["estadoPro"]

            if nome=='' or cpf=='' or profissao=='' or telefone=='' or data_de_nascimento=='' or email=='' or senha=='' or cep=='' or endereco=='' or numero=='' or cidade=='' or estado=='':
                error = 'Preencha todos os campos!'
            elif cpf == "CPF Inválido" or len(cpf) != 14:
                error = 'Verifique seu CPF!'
            elif endereco =="CEP não encontrado":
                error = 'Verifique seu CEP!'
            elif controler.verifica_email(email,'usuarios'):
                error = 'Ops! Email já cadastrado.'
            elif len(data_de_nascimento) != 10  or controler.valida_data(data_de_nascimento) or controler.verifica_idade(data_de_nascimento) == "erro":
                error = 'Data de nascimento inválida'
            elif len(request.form["telefonePro"]) != 14 and len(request.form["telefonePro"]) != 13:
                error = 'Verifique seu telefone!'
            else:
                cpf = controler.limpa_cpf(request.form["cpfPro"])
                if controler.verifica_cpf(cpf, 'usuarios'):
                    if tipo == 0: #update
                        pass
                    else:
                        error = 'Este CPF já está cadastrado!'
                else:
                    hashed_password = generate_password_hash(senha)
                    tipo=2
                    controler.cadastra_usuario(cpf, nome, email, telefone, controler.converte_data(data_de_nascimento), hashed_password, tipo)
                    id_profissional = controler.select("id", "usuarios", "cpf="+str(cpf))[0][0]
                    telefone_comercial=telefone
                    controler.cadastra_profissional(id_profissional, profissao, registro_profissional, telefone_comercial, cep, endereco, numero, complemento, cidade, estado)
                    return redirect(url_for('login'))
    return render_template('create.html', error=error)


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST' and request.form['senha']!='' and request.form['cpf']!='':
        cpf_inserido = controler.limpa_cpf(request.form["cpf"])
        senha_inserida = request.form["senha"]

        if controler.verifica_cpf(cpf_inserido, "usuarios"): # ta na bd
            user = Usuario(controler.cpf_id(cpf_inserido, "usuarios"))
            if check_password_hash(user.senha,senha_inserida):
                session['user'] = True
                session['id'] = user.id
                tipo = controler.cpf_tipo(cpf_inserido, "usuarios")
                if tipo==1:
                    return redirect(url_for('loggedCliente'))

                elif tipo==2:
                    return redirect(url_for('loggedProfissional'))

                elif tipo==3:
                    return redirect(url_for('ProfissionalCliente'))    
            else:
                error = "Senha incorreta!"
        else:
            error = "Usuário não cadastrado"
    return render_template('login.html', error=error)

@app.before_request
def before_request():
    g.user = None
    if g.user in session:
        g.user = session['user']

@app.route('/loggedCliente', methods = ['GET', 'POST'])
def loggedCliente():
    if 'user' in session:
        user = Cliente(session['id'])
        return render_template("loggedCliente.html", cliente=user.nome, tipo = Usuario(session['id']).tipo)
    return redirect(url_for('login'))

@app.route('/loggedProfissional')
def loggedProfissional():
    if 'user' in session:
        user = Profissional(session['id'])
        return render_template("loggedProfissional.html", profissional=user.nome, tipo = Usuario(session['id']).tipo)
    return redirect(url_for('login'))


@app.route('/loggedCliProf', methods=['GET', 'POST'])
def ProfissionalCliente():
    if 'user' in session:
        user = Usuario(session['id'])
        return render_template('ProfissionalCliente.html', nome_usuario=user.nome, tipo = Usuario(session['id']).tipo)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('login', None)
        session.pop('id', None)
    return redirect(url_for('login'))


@app.route('/sobreNos', methods=['GET', 'POST'])
def sobreNos():
    error = None
    if request.method =='POST':
        return redirect(url_for('cadastro'))
    return render_template('sobreNos.html', error=error)

@app.route('/recibosProfissional', methods=['GET', 'POST'])
def RecibosProfissional():
    def sortData(val):
        data = val[4][6:] + val[4][3:5] + val[4][0:2]
        return int(data)
    def sortNome(val): 
        return val[8]
    def sortValor(val): 
        valor = val[3].replace("R$","").replace(",","")
        return int(valor)
    id_profissional = session['id']
    recibos = controler.select("*", "atendimentos", "id_profissional="+id_profissional)
    recibosNew = []
    for recibo in recibos:
        recibo = list(recibo)
        recibo.append(controler.select("nome", "usuarios", "id=" + str(recibo[2]))[0][0])
        recibosNew.append(recibo)
        recibo[4] = recibo[4].strftime("%d/%m/%Y")

    if request.method == "POST": # Handles os ordenadores
        if "data" in request.form:
            recibosNew.sort(key = sortData)
        elif "nome" in request.form:
            recibosNew.sort(key = sortNome)
        elif "valor" in request.form:
            recibosNew.sort(key = sortValor)
        elif "cadastrar" in request.form:
            return redirect(url_for('CadastrarAtendimentos'))
        app.logger.info(recibosNew[0])
    if request.method == "POST":
        dic = request.form.to_dict()
        app.logger.warning(dic)
        dicInvertido = dict(zip(dic.values(),dic.keys()))
        if "Baixar recibo" in dicInvertido :
            index = int(dicInvertido["Baixar recibo"])
            id_atendimento = str(recibosNew[index][0])
            rendered = controler.gerar_pdf(id_atendimento)

            pdf = pdfkit.from_string(rendered, False)

            response =  make_response(pdf)
            response.headers['Content-Type'] =  'applocation/pdf'
            response.headers['Content-Disposition'] =   'inline; filename = recibo' + id_atendimento + '.pdf'

            return response

    return render_template('RecibosProfissional.html', recibos=recibosNew, lenRecibos = len(recibosNew))

@app.route('/recibosCliente', methods=['GET', 'POST'])
def RecibosCliente():
    def sortData(val):
        data = val[4][6:] + val[4][3:5] + val[4][0:2]
        return int(data)
    def sortNome(val): 
        return val[8]
    def sortArea(val): 
        return val[9]
    def sortValor(val): 
        valor = val[3].replace("R$","").replace(",","")
        return int(valor)
    id_cliente = session['id']
    recibos = controler.select("*", "atendimentos", "id_cliente="+id_cliente)
    recibosNew = []
    for recibo in recibos:
        recibo = list(recibo)
        recibo.append(controler.select("nome", "usuarios", "id=" + str(recibo[1]))[0][0])
        recibo.append(controler.select("profissao", "profissionais", "id_profissional=" + str(recibo[1]))[0][0])
        recibosNew.append(recibo)
        recibo[4] = recibo[4].strftime("%d/%m/%Y")
    
    if request.method == "POST": # Handles os ordenadores
        if "data" in request.form:
            recibosNew.sort(key = sortData)
        elif "nome" in request.form:
            recibosNew.sort(key = sortNome)
        elif "area" in request.form:
            recibosNew.sort(key = sortArea)
        elif "valor" in request.form:
            recibosNew.sort(key = sortValor)
    if request.method == "POST":
        dic = request.form.to_dict()
        app.logger.warning(dic)
        dicInvertido = dict(zip(dic.values(),dic.keys()))
        if "Baixar recibo" in dicInvertido :
            index = int(dicInvertido["Baixar recibo"])
            id_atendimento = str(recibosNew[index][0])
            rendered = controler.gerar_pdf(id_atendimento)

            pdf = pdfkit.from_string(rendered, False)

            response =  make_response(pdf)
            response.headers['Content-Type'] =  'applocation/pdf'
            response.headers['Content-Disposition'] =   'inline; filename = recibo' + id_atendimento + '.pdf'

            return response

    return render_template('RecibosCliente.html', recibos=recibosNew)

@app.route('/meusClientes', methods=['GET', 'POST'])
def meusClientes():
    def sortData(val):
        data = val[4][6:] + val[4][3:5] + val[4][0:2]
        return int(data)
    def sortNome(val): 
        return val[8]
    def sortValor(val): 
        valor = val[3].replace("R$","").replace(",","")
        return int(valor)
    id_profissional = session['id']
    atendimentos = controler.select("*", "atendimentos", "id_profissional="+id_profissional)
    clientes = [] #criar lista dos clientes atendidos, só o id
    buffer = []

    for atendimento in atendimentos:
        if atendimento[2] not in buffer:
            clientes.append([atendimento[2]])
            buffer.append(atendimento[2])

    for cliente in clientes:
        cliente.append(controler.select("nome", "usuarios", "id="+str(cliente[0]))[0][0])
        data_ultima_consulta = (controler.ultima_consulta(id_profissional, cliente[0])).strftime("%d/%m/%Y") 
        cliente.append(data_ultima_consulta)    

    if request.method == "POST": # Handles os ordenadores
        if "data" in request.form:
            clientes.sort(key = sortData)
        elif "nome" in request.form:
            clientes.sort(key = sortNome)
        app.logger.info(clientes[0])

    if request.method == "POST":
        dic = request.form.to_dict()
        app.logger.warning(dic)
        dicInvertido = dict(zip(dic.values(),dic.keys()))
        if "+" in dicInvertido :
            index = int(dicInvertido["+"])
            id_cliente = str(clientes[index][0])
            return redirect(url_for("DetalhesCliente", id_cliente = id_cliente))

    return render_template('MeusClientes.html', recibos=clientes, lenRecibos = len(clientes))

@app.route('/DetalhesCliente/<id_cliente>', methods=['GET', 'POST'])
def DetalhesCliente(id_cliente):
    if "user" in session:
        id_profissional = session["id"]
        cliente = Cliente(id_cliente)

        def sortData(val):
            data = val[4][6:] + val[4][3:5] + val[4][0:2]
            return int(data)
        def sortValor(val): 
            valor = val[3].replace("R$","").replace(",","")
            return int(valor)
            
        where = str.format("id_cliente= {} and id_profissional = {}", id_cliente, id_profissional)
        recibos = controler.select("*", "atendimentos", where)
        recibosNew = []
        for recibo in recibos:
            recibo = list(recibo)
            recibosNew.append(recibo)
            recibo[4] = recibo[4].strftime("%d/%m/%Y")
        
        if request.method == "POST": # Handles os ordenadores
            if "data" in request.form:
                recibosNew.sort(key = sortData)
            elif "valor" in request.form:
                recibosNew.sort(key = sortValor)

        return render_template("DetalhesCliente.html", nome_cliente = cliente.nome, telefone_cliente = cliente.telefone, email_cliente = cliente.email, recibos=recibosNew)
    return redirect(url_for('login'))

@app.route('/cadastraAtendimento', methods=['GET', 'POST'])
def CadastrarAtendimentos():
    nome = None
    email = None
    telefone = None
    error = None
    if request.method == 'POST':
        cpf = request.form['cpfCliente']
        if len(cpf) == 14:
            nome = request.form["nome"]
            email = request.form["email"]
            telefone = request.form["telefone"]
            if controler.verifica_cpf(controler.limpa_cpf(cpf),'usuarios'): #Se o usuario está cadastrado, puxa os dados dele
                id_usuarioAtendimento = controler.cpf_id(controler.limpa_cpf(cpf), 'usuarios')
                userAtendimento = Usuario(id_usuarioAtendimento)
                if nome != userAtendimento.nome: #Essa sequência de 3 if's é pra completar o preencher automaticamente
                    nome = userAtendimento.nome
                if email != userAtendimento.email:
                    email = userAtendimento.email
                if telefone != userAtendimento.telefone:
                    telefone = userAtendimento.telefone
                    if len(telefone) == 11:
                        telefone = '({}){}-{}'.format(telefone[0:2],telefone[2:7], telefone[7:])
                    else:
                        telefone = '({}){}-{}'.format(telefone[0:2],telefone[2:6], telefone[6:])

            else: # Se não está cadastrado, semi-cadastra.
                if "botao" in request.form:
                    nome = request.form["nome"]
                    email = request.form["email"]
                    telefone = request.form["telefone"]
                    cpf = controler.limpa_cpf(request.form['cpfCliente'])
                    controler.pre_cadastra(nome, cpf, controler.limpa_telefone(telefone), email)
                    id_usuarioAtendimento = controler.cpf_id(cpf, 'usuarios')
                    controler.cadastra_cliente(id_usuarioAtendimento,'-','-''-','-','-','-','-','-','-') 
                     #Se o cliente n tá cadastrado, é criado um semi-cadastro e depois o id_cliente dele é puxado

            id_profissional = session['id']
            data_consulta = request.form['dataConsulta']
            data_gerado = date.today()  #para transformar de date em dd/mm/aaa -> .strftime("%d/%m/%Y")
            valor = request.form['valor']
            forma_pagamento = request.form.get('forma_pagamento')
            numero_parcelas = request.form['numero_parcelas']

            if request.form["cpfCliente"] != "" and request.form["nome"] != "" and request.form["email"] != "" and request.form["telefone"] != "" and request.form["dataConsulta"] != "" and request.form["valor"] != "" and forma_pagamento !="0" and numero_parcelas!="":
                controler.cadastra_atendimento(id_profissional, id_usuarioAtendimento, valor, controler.converte_data(data_consulta), data_gerado, int(forma_pagamento), int(numero_parcelas))
                return redirect(url_for('RecibosProfissional')) 
            else:
                if "botao" in request.form:
                    error = "Preencha todos os campos"
    return render_template('CadastrarAtendimentos.html', nome=nome, email=email, telefone=telefone, error=error)

@app.route('/infoProfissional', methods=['GET', 'POST'])
def Informacoes_cadastroPro():
    telefone = Profissional(session['id']).telefone
    if len(telefone) == 11:
        telefone = '({}) {}-{}'.format(telefone[0:2],telefone[2:7], telefone[7:])
    else:
        telefone = '({}) {}-{}'.format(telefone[0:2],telefone[2:6], telefone[6:])
    return render_template('Informacoes_cadastroPro.html', nome=Profissional(session['id']).nome, cpf=Profissional(session['id']).cpf, profissao=Profissional(session['id']).profissao, registro=Profissional(session['id']).registro_profissional, telefone=telefone, nascimento=Profissional(session['id']).data_de_nascimento, email=Profissional(session['id']).email, cep=Profissional(session['id']).cep, endereco=Profissional(session['id']).endereco, numero=Profissional(session['id']).numero, complemento=Profissional(session['id']).complemento, cidade=Profissional(session['id']).cidade, estado=Profissional(session['id']).estado)

@app.route('/infoCliente', methods=['GET', 'POST'])
def Informacoes_cadastroCliente():
    telefone = Cliente(session['id']).telefone
    if len(telefone) == 11:
        telefone = '({}) {}-{}'.format(telefone[0:2],telefone[2:7], telefone[7:])
    else:
        telefone = '({}) {}-{}'.format(telefone[0:2],telefone[2:6], telefone[6:])
    cpf = Cliente(session['id']).cpf
    cpf = '{}.{}.{}-{}'.format(cpf[0:3],cpf[3:6],cpf[6:9],cpf[9:])

    return render_template('Informacoes_cadastroCliente.html', nome=Cliente(session['id']).nome, cpf=cpf, telefone=telefone, nascimento=Cliente(session['id']).data_de_nascimento, email=Cliente(session['id']).email, cep=Cliente(session['id']).cep, endereco=Cliente(session['id']).endereco, numero=Cliente(session['id']).numero, complemento=Cliente(session['id']).complemento, cidade=Cliente(session['id']).cidade, estado=Cliente(session['id']).estado)

#CONFIGURAÇÃO DO EMAIL
app.config['DEBUG']=True
app.config['TESTING']=False
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USE_SSL']=False
#app.config['MAIL_DEBUG']=True
app.config['MAIL_USERNAME']='waat.ufrj@gmail.com'
app.config['MAIL_PASSWORD']='PipocaSalgada!'
app.config['MAIL_DEFAULT_SENDER']=('Equipe WAAT', 'waat.ufrj@gmail.com')
app.config['MAIL_MAX_EMAILS']=3 #NÃO MEXAM AQUI
#app.config['MAIL_SUPRESS_SEND']=False
app.config['MAIL_ASCII_ATTACHMENTS']=True

mail = Mail(app)

@app.route('/esqueciminhasenha', methods=['GET', 'POST'])
def esqueci():
    error = None
    sucesso = None
    if request.method == "POST":
        if "submit" in request.form:
            cpf = request.form["cpfForgot"]
            chave = str(uuid.uuid4())
            datahora = datetime.now()
            controler.cadastra_esquecimento(controler.limpa_cpf(cpf), chave, datahora)

            email = controler.email_user(cpf)[0]
            msg = Message("Recuperação de Senha", recipients=[email])
            link = 'http://127.0.0.1:5000/redefinir/'+chave
            msg.html= render_template('email_recuperarSenha.html', link = link)
            mail.send(msg)
            return redirect(url_for('login'))
            
    return render_template('esqueci_senha.html', error=error, sucesso=sucesso)

@app.route('/redefinir/<token>', methods=['GET', 'POST'])
def redf(token):
    error = None
    if request.method == 'POST':
        if controler.valida_token(token):
            senhanova = request.form['senhanova']
            confirma_senhanova = request.form['confirma_senhanova']
            if senhanova == confirma_senhanova:
                hashed_nova = generate_password_hash(senhanova)
                cpf = controler.select('cpf', 'pedido_mudanca_senha', 'chave= "'+token+'"')[0][0]
                if controler.verifica_cpf(cpf, 'usuarios'):
                    ups = {'senha':hashed_nova}
                    controler.update(ups, "usuarios", "cpf="+cpf)
                return redirect(url_for('login'))
            else:
                error = "As senhas não conferem."
        else:
            error = "O token expirou."
    return render_template('redefinir_senha.html', error = error)   

@app.route('/enviaEmail/')
def enviaEmail(email):
    msg = Message("Recibo", recipients=[email])
    msg.body= "Segue em anexo o recibo referente à sua consulta."

    with app.open_resource("recibo_teste.pdf") as recibo:
        msg.attach("recibo_teste.pdf", "application/pdf", recibo.read())
    mail.send(msg)


if __name__ == '__main__':
    app.run(debug=True)

