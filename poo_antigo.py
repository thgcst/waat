class Usuario():

    def __init__(self, id):
        self.id = str(id)
        
        dados = controler.select_CursorDict('*', 'usuarios', 'id_usuario='+self.id)[0]
        self.nome = dados['nome']
        self.data_de_nascimento = dados['data_de_nascimento']
        self.cpf = dados['cpf']
        self.telefone = dados['telefone']
        self.email = dados['email']
        self.senha = dados['senha']
        self.tipo = dados['tipo']

    def up_nome(self, nome):
        controler.update({'nome':nome}, 'clientes', 'id_cliente='+self.id)
        self.nome = controler.select('nome', 'clientes', 'id_cliente='+self.id)[0][0]

    def up_senha(self, senha):
        controler.update({'senha':senha}, 'clientes', 'id_cliente='+self.id)
        self.senha = controler.select('senha', 'clientes', 'id_cliente='+self.id)[0][0]


class Profissional(Usuario):
    def __init__(self,id):
        super().__init__(id)                              #Usando o fato de ser subclasse e herdando metodos e atributos da classe mãe
        dados = controler.select_CursorDict('*', 'profissionais', 'id_profissional='+self.id)[0]
        self.nome = dados['nome']
        self.profissao = dados['profissao']
        self.registro_profissional = dados['registro_profissional']
        self.cpf = dados['cpf']
        self.telefone = dados['telefone']
        self.data_de_nascimento = dados['data_de_nascimento']
        self.email = dados['email']
        self.senha = dados['senha']
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
