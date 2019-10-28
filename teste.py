from datetime import date

def formato_telefone(telefone):
    if len(telefone) == 14:
        if telefone[0] == "(" and telefone[3] == ")" and telefone[9] =='-':
            return True
        else:
            return False
    elif len(telefone) == 13:
        if telefone[0] == "(" and telefone[3] == ")" and telefone[8] =='-':
            return True
        else:
            return False
    return False

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

def valida_data(data):
    '''Checa se a data inserida é maior que a data atual, logo é inválida'''
    hoje = date.today()
    hoje = int(str(hoje.year) + str(hoje.month) + str(hoje.day))
    data = int(data[6:] + data[3:5] + data[0:2])
    return data > hoje

data_de_nascimento = "31/09/1999"

result = len(data_de_nascimento) != 10 or valida_data(data_de_nascimento) or verifica_idade(data_de_nascimento) == "erro"

print(result)