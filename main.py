import peewee
from peewee import *

db = peewee.MySQLDatabase(
	host='127.0.0.1', 
	user='root', 
	passwd='',
	database='capitolio')

class BaseModel(Model):
    class Meta:
        database = db
		
class clp_tb_empresas(BaseModel):
	id_empresa = IntegerField(unique=True)
	nome_empresa = TextField()
	razao_social = TextField()
	endereco = TextField()
	cep = TextField()
	cidade = TextField()
	estado = TextField()
	telefone = TextField()
	fax = TextField()
	observacao = TextField()
	contato_titulo = TextField()
	contato_nome = TextField()
	contato_cargo = TextField()
	contato_telefone = TextField()
	contato_celular = TextField()
	contato_email = TextField()
	contato_financ_titulo = TextField()
	contato_financ_nome = TextField()
	contato_financ_cargo = TextField()
	contato_financ_telefone = TextField()
	contato_financ_celular = TextField()
	contato_financ_email = TextField()
	tipo_envio = IntegerField(default=0)

class clp_tb_clientes(BaseModel):
	id_cliente = AutoField()
	empresa = ForeignKeyField(clp_tb_empresas)
	nome_cliente = TextField()
	titulo_cliente = TextField()
	cargo_cliente = TextField()
	dddf_cliente = TextField()
	telf_cliente = TextField()
	dddc_cliente = TextField()
	telc_cliente = TextField()
	email_cliente = TextField()
	observacoes_cliente = TextField()
	tipo_envio = IntegerField()
	Habilitado = IntegerField(default=1)




for clientes in clp_tb_clientes.select():
    print(clientes.id_cliente, clientes.nome_cliente, clientes.empresa.nome_empresa)

