import random
import mysql.connector
from datetime import date

config = {
  'user': 'sql10309123',
  'password': 'amsv6YKy6N',
  'host': 'sql10.freesqldatabase.com',
  'database': 'sql10309123',
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

def insert(values, table, fields =None):
    global cursor,  con
    query = "INSERT INTO " +table
    if (fields):
        query += " ("+ fields + ") "
    query += " VALUES " + ",".join(["("+v+")" for v in values])
    cursor.execute(query)
    con.commit()

def update(sets, table, where=None):
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

def verifica_cpf(cpf, tabela):
    """retorna True se o cpf já está cadastrado e False c.c."""
    cpf = "cpf="+str(cpf)
    cpf_no_db = bool(len(select("cpf", tabela, cpf)))
    return cpf_no_db

def verifica_email(email, tabela):
    """retorna True se o email já está cadastrado e False c.c."""
    email = "email="+str(email)
    email_no_db = bool(len(select("email", tabela, email)))
    return email_no_db
    
def cpf_senha(cpf, tabela):
    """Retorna a senha correspondente ao cpf"""
    cpf = "cpf="+str(cpf)
    senha = select("senha", tabela, cpf)
    return senha[0][0]

def verifica_idade(data_de_nascimento):
    hoje = date.today()
    nascimento = date(int(data_de_nascimento[6:]),int(data_de_nascimento[3:5]),int(data_de_nascimento[:2]))
    idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (hoje.month, hoje.day))
    if idade<18:
        return True
    else:
        return False
        
def cpf_id(cpf, tabela):
    """Retorna a senha correspondente ao cpf"""
    cpf = "cpf="+str(cpf)
    if tabela == 'clientes':
        id = select("id_cliente", tabela, cpf)
        return id[0][0]
    else:
        id = select("id_profissional", tabela, cpf)
        return id[0][0]

def gera_id():
    id_gerado = random.randint(1,100)
    id_no_bd = (verifica_id_cliente(id_gerado) and verifica_id_profissional(id_gerado))
    while id_no_bd:        
        id_gerado = random.randint(1,100)
        id_no_bd = (verifica_id_cliente(id_gerado) and verifica_id_profissional(id_gerado))
    return id_gerado


def cadastra_cliente(nome, data_de_nascimento, cpf, telefone, email, senha, cep, endereco, numero, complemento, cidade, estado, nome_responsavel, cpf_responsavel):
    id_cliente = gera_id()
    sql = "INSERT INTO clientes (id_cliente, nome, data_de_nascimento, cpf, telefone, email, senha, cep, endereco, numero, complemento, cidade, estado, nome_responsavel, cpf_responsavel) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    data = (id_cliente, nome, data_de_nascimento, cpf, telefone, email, senha, cep, endereco, numero, complemento, cidade, estado, nome_responsavel, cpf_responsavel)
    cursor.execute(sql, data)
    con.commit()


def cadastra_profissional(nome, cpf, profissao, registro_profissional, telefone, data_de_nascimento, email, senha, cep, endereco, numero, complemento, cidade, estado, assinatura='-'):
    id_profissional = gera_id()
    sql = "INSERT INTO profissionais (id_profissional, nome, cpf, profissao, registro_profissional, telefone, data_de_nascimento, email, senha, cep, endereco, numero, complemento, cidade, estado, assinatura) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    data = (id_profissional, nome, cpf, profissao, registro_profissional, telefone, data_de_nascimento, email, senha, cep, endereco, numero, complemento, cidade, estado)
    cursor.execute(sql, data)
    con.commit()
