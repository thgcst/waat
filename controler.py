import random
import MySQLdb

host = 'sql10.freesqldatabase.com'
user = 'sql10308309'
senha = 'rPgCW78Vu7'
db = 'sql10308309'
port = 3306

con = MySQLdb.Connect(host, user, senha, db, port)
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
    query += " SET " + ",".join([field+ " = " + value +"'" for field, value in sets.item()])
    if (where):
        query += " WHERE " + where  
    cursor.execute(query)
    con.commit()
    
def delete(table, where):
    global cursor,  con
    query = "DELETE FROM "+ table +" WHERE "+where
    cursor.execute(query)
    con.commit()

def verifica_cpf(cpf, tabela):
    """retorna True se o cpf já está cadastrado e False c.c."""
    cpf = "cpf="+str(cpf)
    cpf_no_db = bool(len(select("cpf", tabela, cpf)))
    return cpf_no_db
    
def cpf_senha(cpf, tabela):
    """Retorna a senha correspondente ao cpf"""
    cpf = "cpf="+str(cpf)
    senha = select("senha", tabela, cpf)
    return senha[0][0]

def gera_id_cliente():
    id_gerado = random.randint(1,100000)
    id = "id_cliente="+str(id_gerado)
    id_na_bd = bool(len(select("id_cliente", "clientes", id)))
    while id_na_bd:        
        id_gerado = random.randint(1,100000)
        id = "id_cliente="+str(id_gerado)
        id_na_bd = bool(len(select("id_cliente", "clientes", id)))
    return id_gerado


def gera_id_profissional():
    id_gerado = random.randint(1,100000)
    id = "id_profissional="+str(id_gerado)
    id_na_bd = bool(len(select("id_profissional", "profissionais", id)))
    while id_na_bd:        
        id_gerado = random.randint(1,100000)
        id = "id_profissional="+str(id_gerado)
        id_na_bd = bool(len(select("id_profissional", "profissionais", id)))
    return id_gerado


def cadastra_cliente_adulto(nome, data_de_nascimento, cpf, telefone, endereco, email, senha):
    id_cliente = gera_id_cliente()
    sql = "INSERT INTO clientes (id_cliente, nome, data_de_nascimento, cpf, telefone, endereco, email, senha) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
    data = (id_cliente, nome, data_de_nascimento, cpf, telefone, endereco, email, senha)
    cursor.execute(sql, data)
    con.commit()

def cadastra_cliente_menor(nome, data_de_nascimento, cpf, telefone, endereco, email, senha, cpf_responsavel, nome_responsavel):
    id_cliente = gera_id_cliente()
    sql = "INSERT INTO clientes (id_cliente, nome, data_de_nascimento, cpf, telefone, endereco, email, senha, cpf_responsavel, nome_responsavel) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    data = (id_cliente, nome, data_de_nascimento, cpf, telefone, endereco, email, senha, cpf_responsavel, nome_responsavel)
    cursor.execute(sql, data)
    con.commit()
#em progresso
def cadastra_profissional(nome, cpf, profissao, endereco_comercial, email, registro_profissional, telefone, senha):
    id_profissional = gera_id_profissional()
    sql = "INSERT INTO profissionais (id_profissional, nome, cpf, profissao, endereco_comercial, email, registro_profissional, telefone, senha) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    data = (id_profissional, nome, cpf, profissao, endereco_comercial, email, registro_profissional, telefone, senha)
    cursor.execute(sql, data)
    con.commit()