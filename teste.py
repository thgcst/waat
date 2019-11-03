from datetime import date

# a = 21

# a = "0" + str(a)

# a = a[-2:]

# print(a)

def valida_data(data):
    '''Checa se a data inserida é maior que a data atual, logo é inválida'''
    hoje = date.today()
    hoje = int(str(hoje.year) + ("0" + str(hoje.month))[-2:] + ("0" + str(hoje.day))[-2:])
    data = int(data[6:] + data[3:5] + data[0:2])
    return data > hoje

valida_data("01/12/1999")
