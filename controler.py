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


def cadastra_cliente(nome, data_de_nascimento, cpf, telefone, email, senha, cep, endereco, numero, complemento, cidade, estado, nome_responsavel, cpf_responsavel):
    id_cliente = gera_id_cliente()
    sql = "INSERT INTO clientes (id_cliente, nome, data_de_nascimento, cpf, telefone, email, senha, cep, endereco, numero, complemento, cidade, estado, nome_responsavel, cpf_responsavel) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    data = (id_cliente, nome, data_de_nascimento, cpf, telefone, email, senha, cep, endereco, numero, complemento, cidade, estado, nome_responsavel, cpf_responsavel)
    cursor.execute(sql, data)
    con.commit()


def cadastra_profissional(nome, cpf, profissao, registro_profissional, telefone, data_de_nascimento, email, senha, cep, endereco, numero, complemento, cidade, estado):
    id_profissional = gera_id_profissional()
    sql = "INSERT INTO profissionais (id_profissional, nome, cpf, profissao, registro_profissional, telefone, data_de_nascimento, email, senha, cep, endereco, numero, complemento, cidade, estado) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    data = (id_profissional, nome, cpf, profissao, registro_profissional, telefone, data_de_nascimento, email, senha, cep, endereco, numero, complemento, cidade, estado)
    cursor.execute(sql, data)
    con.commit()