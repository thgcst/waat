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
