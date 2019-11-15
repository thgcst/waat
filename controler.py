import random
import mysql.connector
from flask import render_template, make_response
import pdfkit
from datetime import date, datetime, timedelta

config = {
  'user': 'sql10311918',
  'password': 'eWHrsSjmIQ',
  'host': 'sql10.freesqldatabase.com',
  'database': 'sql10311918',
  'port': '3306'}

con = mysql.connector.connect(**config)
cursor = con.cursor()

def select(fields, tables, where = None):
    global cursor
    query = "SELECT " + fields + " FROM " +tables
    if (where):
        query += " WHERE " + where
    cursor.execute(query)
    return cursor.fetchall()

def exist(cpf, table):
    global cursor
    query = "SELECT COUNT(nome) FROM " + table +" WHERE cpf="+cpf;
    cursor.execute(query)
    return bool(cursor.fetchall()[0][0])

def insert(values, table, fields =None):
    global cursor,  con
    query = "INSERT INTO " +table
    if (fields):
        query += " ("+ fields + ") "
    query += " VALUES " + ",".join(["("+v+")" for v in values])
    cursor.execute(query)
    con.commit()

def update(sets, table, where):
    global cursor,  con
    query = "UPDATE " +table
    query += " SET " + ",".join([field+ " = '" + value + "'" for field, value in sets.items()])
    if (where):
        query += " WHERE " + where
    cursor.execute(query)
    con.commit()

def delete(table, where):
    global cursor,  con
    query = "DELETE FROM "+ table +" WHERE "+where
    cursor.execute(query)
    con.commit()

def limpa_telefone(telefone):
    if len(telefone)==14:
        ddd = telefone[1:3]
        bloco5 = telefone[4:9]
        bloco4 = telefone[10:]
        return ddd+bloco5+bloco4
    
    if len(telefone)==13:
        ddd = telefone[1:3]
        bloco1 = telefone[4:8]
        bloco2 = telefone[9:]
        return ddd+bloco1+bloco2

def limpa_cpf(cpf):
    '''Limpa o CPF, tirando ponto e traço'''
    first = cpf[:3]
    second = cpf[4:7]
    third = cpf[8:11]
    final =cpf[12:]
    return first+second+third+final

def valida_cpf(cpf):
    '''Faz a validação do cpf inserido. Retorna True se for válido e False se for inválido'''
    cpf_limpo = limpa_cpf(cpf)

    digitos=[]
    for i in range (0, 11):
        digitos.append(int(cpf_limpo[i]))
    
    primeiro_validador = 0
    for i in range (0, 9):
        buffer = (10-i)*digitos[i]
        primeiro_validador += buffer
    primeiro_resto = primeiro_validador%11    

    if primeiro_resto<2:
        primeiro_digito = 0
    else:
        primeiro_digito = 11-primeiro_resto
    
    if primeiro_digito != digitos[9]:
        return False

    segundo_validador=0

    for i in range (0, 10):
        buffer = (11-i)*digitos[i]
        segundo_validador += buffer
    segundo_resto = segundo_validador%11

    if segundo_resto<2:
        segundo_digito=0
    else:
        segundo_digito = 11-segundo_resto

    if segundo_digito != digitos[10]:
        return False

    return True

def verifica_id_cliente(id):
    """retorna True se o id_cliente já está cadastrado e False c.c."""
    id = "id_cliente="+str(id)
    id_no_bd = bool(len(select("id_cliente", 'clientes', id)))
    return id_no_bd

def verifica_id_profissional(id):
    """retorna True se o id_profissional já está cadastrado e False c.c."""
    id = "id_profissional="+str(id)
    id_no_bd = bool(len(select("id_profissional", 'profissionais', id)))
    return id_no_bd

def verifica_id_atendimento(id):
    """retorna True se o atendimento já está cadastrado e False c.c."""
    id = "id_atendimento="+str(id)
    id_no_bd = bool(len(select("id_atendimento", 'atendimentos', id)))
    return id_no_bd

def verifica_cpf(cpf, tabela):
    """retorna True se o cpf já está cadastrado e False c.c."""
    cpf = "cpf="+str(cpf)
    cpf_no_db = bool(len(select("cpf", tabela, cpf)))
    return cpf_no_db

def separa_email(email):
    user_mail = email.split('@')[0]
    domain_mail = email.split('@')[1]
    return user_mail, domain_mail
    
def cpf_senha(cpf, tabela):
    """Retorna a senha correspondente ao cpf"""
    cpf = "cpf="+str(cpf)
    senha = select("senha", tabela, cpf)
    return senha[0][0]

def verifica_idade(data_de_nascimento):
    hoje = date.today()
    try:
        nascimento = date(int(data_de_nascimento[6:]),int(data_de_nascimento[3:5]),int(data_de_nascimento[:2]))
    except:
        return "erro"
    idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (hoje.month, hoje.day))

    if idade<18:
        return True
    else:
        return False
        
def cpf_id(cpf, tabela):
    """Retorna o id correspondente ao cpf"""
    cpf = "cpf="+str(cpf)
    id = select("id", tabela, cpf)
    return id[0][0]

def cpf_tipo(cpf, tabela):
    """Retorna o id correspondente ao cpf"""
    cpf = "cpf="+str(cpf)
    tipo = select("tipo", tabela, cpf)
    return tipo[0][0]


def gera_id():
    id_gerado = random.randint(1,100)
    id_no_bd = (verifica_id_cliente(id_gerado) or verifica_id_profissional(id_gerado) or verifica_id_atendimento(id_gerado))
    while id_no_bd:        
        id_gerado = random.randint(1,100)
        id_no_bd = (verifica_id_cliente(id_gerado) or verifica_id_profissional(id_gerado) or verifica_id_atendimento(id_gerado))
    return id_gerado

def email_user(cpf):
    cpf = limpa_cpf(cpf)
    error = None
    if exist(cpf, 'usuarios'):
        error='enviado'
        email = select('email', 'usuarios', 'cpf='+cpf)[0][0]
        return (email,error)
    else:
        error = "Não cadastrado"
        return (None, error)

def ApenasUpdate(cpf, table):
    if exist(limpa_cpf(cpf),'clientes'):
        ApenasUpdate = True  #update
    else:
        ApenasUpdate = False #cadastro normal  

def cadastra_usuario(cpf, nome, email, telefone, data_de_nascimento, senha, tipo):
    user_mail = separa_email(email)[0]
    domain_mail = separa_email(email)[1]
    sql = "INSERT INTO usuarios (id, cpf, nome, email, user_mail, domain_mail, telefone, data_de_nascimento, senha, tipo) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    data = ('DEFAULT', cpf, nome, email, user_mail, domain_mail, telefone, data_de_nascimento, senha, tipo)
    cursor.execute(sql, data)
    con.commit()

def cadastra_cliente(id_cliente, cep, endereco, numero, complemento, cidade, estado, nome_responsavel, cpf_responsavel):
    sql = "INSERT INTO clientes (id_cliente, cep, endereco, numero, complemento, cidade, estado, nome_responsavel, cpf_responsavel) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    data = (id_cliente, cep, endereco, numero, complemento, cidade, estado, nome_responsavel, cpf_responsavel)
    cursor.execute(sql, data)
    con.commit()

def cadastra_profissional(id_profissional, profissao, registro_profissional, telefone_comercial, cep, endereco, numero, complemento, cidade, estado):
    if registro_profissional == "":
        registro_profissional = "-"
    if telefone_comercial == "":
        telefone_comercial == ""
    sql = "INSERT INTO profissionais (id_profissional, profissao, registro_profissional, telefone_comercial, cep, endereco, numero, complemento, cidade, estado) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    data = (id_profissional, profissao, registro_profissional, telefone_comercial, cep, endereco, numero, complemento, cidade, estado)
    cursor.execute(sql, data)
    con.commit()

def cadastra_atendimento(id_profissional, id_cliente, valor, data_consulta, data_gerado, forma_pagamento, numero_parcelas):
    sql = "INSERT INTO atendimentos (id_atendimento, id_profissional, id_cliente, valor, data_consulta, data_gerado,forma_pagamento, numero_parcelas) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
    data = ('DEFAULT', id_profissional, id_cliente, valor, data_consulta, data_gerado,forma_pagamento, numero_parcelas)
    cursor.execute(sql, data)
    con.commit()

def cadastra_esquecimento(cpf, chave, datahora):
    sql = "INSERT INTO pedido_mudanca_senha (id_pedido, cpf, chave,datahora) VALUES(%s,%s,%s,%s)"
    data = ('DEFAULT', cpf, chave, datahora)
    cursor.execute(sql, data)
    con.commit()

def pre_cadastra(nome, cpf, telefone, email):
    user_mail = separa_email(email)[0]
    domain_mail = separa_email(email)[1]
    data_de_nascimento = '-'
    senha = '-'
    tipo = 0
    sql = "INSERT INTO usuarios (id, cpf, nome, email, user_mail, domain_mail, telefone, data_de_nascimento, senha, tipo) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    data = ('DEFAULT', cpf, nome, email, user_mail, domain_mail, telefone, data_de_nascimento, senha, tipo)
    cursor.execute(sql, data)
    con.commit()

def completa_cadastro_cliente(nome, data_de_nascimento, cpf, telefone, email, senha, cep, endereco, numero, complemento, cidade, estado, nome_responsavel, cpf_responsavel):
    id_cliente = cpf_id(cpf, 'usuarios')
    ups_usuario = {'nome':nome, 'data_de_nascimento':data_de_nascimento, 'telefone':telefone, 'email':email, 'user_mail':user_mail, 'domain_mail':domain_mail, 'senha':senha, 'cep':cep, 'endereco':endereco, 'numero':numero, 'complemento':complemento, 'cidade':cidade, 'estado':estado, 'nome_responsavel':nome_responsavel, 'cpf_responsavel':cpf_responsavel}
    update(ups,'clientes','id_cliente='+str(id_cliente))

def completa_cadastro_profissional():
    pass


def select_CursorDict(fields, tables, where = None):
    cursor = con.cursor(dictionary = True) 

    query = "SELECT " + fields + " FROM " +tables

    if (where):
        query += " WHERE " + where
    cursor.execute(query)
    return cursor.fetchall()

def verifica_email(email, table):
    lista_DomainUser = str.split(email, '@')
    user_mail = "'"+ lista_DomainUser[0] +"'"
    domain_mail = "'" +lista_DomainUser[1]+"'"
    query = "select count(user_mail) from {} where domain_mail = {} and user_mail = {} ;".format(table, domain_mail, user_mail)
    cursor.execute(query)
    return bool(cursor.fetchall()[0][0])

def valida_data(data):
    '''Checa se a data inserida é maior que a data atual, logo é inválida'''
    hoje = date.today()
    hoje = int(str(hoje.year) + ("0" + str(hoje.month))[-2:] + ("0" + str(hoje.day))[-2:])
    data = int(data[6:] + data[3:5] + data[0:2])
    return data > hoje

def gerar_pdf(id_atendimento):
    id_profissional = str(select("id_profissional", "atendimentos", "id_atendimento="+id_atendimento)[0][0])
    id_cliente = str(select("id_cliente", "atendimentos", "id_atendimento = " + id_atendimento)[0][0])
    nomeProfissional = select("nome", "profissionais" , "id_profissional = " + id_profissional)[0][0]
    regProf = select("registro_profissional", "profissionais" , "id_profissional = " + id_profissional)[0][0]
    profissao = select("profissao", "profissionais" , "id_profissional = " + id_profissional)[0][0]
    nome = select("nome", "clientes" , "id_cliente = " + id_cliente)[0][0]
    cpf = select("cpf", "clientes" , "id_cliente = " + id_cliente)[0][0]
    cpf = '{}.{}.{}-{}'.format(cpf[0:3],cpf[3:6],cpf[6:9],cpf[9:])
    cpfRes = select("cpf_responsavel", "clientes" , "id_cliente = " + id_cliente)[0][0]
    cpfRes = '{}.{}.{}-{}'.format(cpfRes[0:3],cpfRes[3:6],cpfRes[6:9],cpfRes[9:])
    nomeRes = select("nome_responsavel", "clientes" , "id_cliente = " + id_cliente)[0][0]
    precoConsulta = select("valor", "atendimentos", "id_atendimento = " + id_atendimento)[0][0]
    email = select("email", "profissionais" , "id_profissional = " + id_profissional)[0][0]
    enderecoComercial = select("endereco", "profissionais" , "id_profissional = " + id_profissional)[0][0] + "" + select("numero", "profissionais" , "id_profissional = " + id_profissional)[0][0] + ", " + select("endereco", "profissionais" , "id_profissional = " + id_profissional)[0][0]
    telefone = select("telefone", "profissionais" , "id_profissional = " + id_profissional)[0][0]
    if len(telefone) == 11:
        telefone = '({}){}-{}'.format(telefone[0:2],telefone[2:7], telefone[7:])
    else:
        telefone = '({}){}-{}'.format(telefone[0:2],telefone[2:6], telefone[6:])
    cep = select("cep", "profissionais" , "id_profissional = " + id_profissional)[0][0]
    dataDoAtendimento = select("data_consulta", "atendimentos" , "id_atendimento = " + id_atendimento)[0][0]

    if nomeRes == '-' or nomeRes == None:
        rendered = render_template('pdf_template18+.html', nomeProfissional = nomeProfissional, regProf = regProf, profissao = profissao, nome = nome, cpf = cpf, precoConsulta = precoConsulta, email=email, enderecoComercial = enderecoComercial, telefone = telefone, cep = cep, dataDoAtendimento = dataDoAtendimento)
    else:
        rendered = render_template('pdf_template18-.html', nomeProfissional = nomeProfissional, regProf = regProf, profissao = profissao, nome = nome, cpfRes = cpfRes, nomeRes = nomeRes, precoConsulta = precoConsulta, email=email, enderecoComercial = enderecoComercial, telefone = telefone, cep = cep , dataDoAtendimento = dataDoAtendimento)

    return rendered


def valida_token(token):
    data_registro = select('datahora', 'pedido_mudanca_senha', 'chave= "'+token+'"')[0][0]
    data_agora = datetime.now()
    validacao = (data_agora - data_registro)
    return validacao<timedelta(days=1)

def converte_dataNascimento(data):
    dia = int(data[:2])
    mes = int(data[3:5])
    ano = int(data[6:])
    data = date(ano, mes, dia)
    return data

recibo = select("*", "atendimentos", "id_profissional=4")[1]
print(select("nome", "usuarios", "id=" + str(recibo[2]))[0][0])