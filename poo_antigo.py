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