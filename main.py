import peewee
from peewee import *

db = peewee.MySQLDatabase(
	host='127.0.0.1', 
	user='root', 
	passwd='',
	database='dbname')

class BaseModel(Model):
    class Meta:
        database = db
		
class Empresa(BaseModel):
	id_empresa = PrimaryKeyField()
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
	
	class Meta:
		table_name = 'clp_tb_empresas'
		
class Cliente(BaseModel):
	id_cliente = PrimaryKeyField()
	id_empresa = IntegerField()
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
	empresa = ForeignKeyField(Empresa, db_column='id_empresa')
	
	class Meta:
		table_name = 'clp_tb_clientes'

class Produto(BaseModel):
	id_produto = PrimaryKeyField()
	nome_produto = TextField()
	tipo = TextField()
	template = TextField()
	
	class Meta:
		table_name = 'clp_tb_produtos'

class Informe(BaseModel):
	id_informe = PrimaryKeyField()
	id_produto = IntegerField()
	data = TextField()
	remetente = TextField()
	titulo = TextField()
	corpo = TextField()
	template = TextField()
	id_usuario = IntegerField()
	produto = ForeignKeyField(Produto, db_column='id_produto')
	
	class Meta:
		table_name = 'clp_tb_informes'

class InformeLog(BaseModel):
	id_informe = IntegerField()
	id_cliente = IntegerField()
	status = TextField()
	tentativas = IntegerField()
	cliente = ForeignKeyField(Cliente, db_column='id_cliente')
	informe = ForeignKeyField(Informe, db_column='id_informe')
	
	class Meta:
		primary_key = False
		table_name = 'clp_tb_informe_log'

#for cliente in Cliente.select():
	#print(cliente.nome_cliente)

#for informe in Informe.select():
#	print(informe.titulo, informe.remetente, informe.produto.nome_produto)

#for cliente in Cliente.select():
#	print('ID [{}] Nome [{}] Empresa[{}]'.format(cliente.id_cliente,cliente.nome_cliente, cliente.empresa.nome_empresa))
a = 0
for informeLog in InformeLog.select():
	print(informeLog.tentativas, informeLog.status, informeLog.cliente.nome_cliente, informeLog.informe.titulo)
	a = a + 1
	print(a)
	print(informeLog.tentativas)
print(a)