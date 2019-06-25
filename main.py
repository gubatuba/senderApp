import secureProperties
import html
import peewee
from peewee import *
from emailSend import emailSend

db = peewee.MySQLDatabase(
	host='127.0.0.1', 
	user='root', 
	passwd='',
	database='dbname')

class BaseModel(Model):
    class Meta:
        database = db
		
class Empresa(BaseModel):
	id = PrimaryKeyField(db_column='id_empresa')
	nome_empresa = TextField(db_column='nome_empresa')
	razao_social = TextField(db_column='razao_social')
	endereco = TextField(db_column='endereco')
	cep = TextField(db_column='cep')
	cidade = TextField(db_column='cidade')
	estado = TextField(db_column='estado')
	telefone = TextField(db_column='telefone')
	fax = TextField(db_column='fax')
	observacao = TextField(db_column='observacao')
	contato_titulo = TextField(db_column='contato_titulo')
	contato_nome = TextField(db_column='contato_nome')
	contato_cargo = TextField(db_column='contato_cargo')
	contato_telefone = TextField(db_column='contato_telefone')
	contato_celular = TextField(db_column='contato_celular')
	contato_email = TextField(db_column='contato_email')
	contato_financeiro_titulo = TextField(db_column='contato_financ_titulo')
	contato_financeiro_nome = TextField(db_column='contato_financ_nome')
	contato_financeiro_cargo = TextField(db_column='contato_financ_cargo')
	contato_financeiro_telefone = TextField(db_column='contato_financ_telefone')
	contato_financeiro_celular = TextField(db_column='contato_financ_celular')
	contato_financeiro_email = TextField(db_column='contato_financ_email')
	tipo_envio = IntegerField(default=0, db_column='tipo_envio')
	
	class Meta:
		table_name = 'clp_tb_empresas'
		
class Cliente(BaseModel):
	id = PrimaryKeyField(db_column='id_cliente')
	empresa_id = IntegerField(db_column='id_empresa')
	nome = TextField(db_column='nome_cliente')
	titulo = TextField(db_column='titulo_cliente')
	cargo = TextField(db_column='cargo_cliente')
	ddd_fixo = TextField(db_column='dddf_cliente')
	fixo = TextField(db_column='telf_cliente')
	ddd_celular = TextField(db_column='dddc_cliente')
	celular = TextField(db_column='telc_cliente')
	email = TextField(db_column='email_cliente')
	observacoes = TextField(db_column='observacoes_cliente')
	tipo_envio = IntegerField(db_column='tipo_envio')
	habilitado = IntegerField(default=1, db_column='Habilitado')
	empresa = ForeignKeyField(Empresa, db_column='id_empresa')
	
	class Meta:
		table_name = 'clp_tb_clientes'

class Produto(BaseModel):
	id = PrimaryKeyField(db_column='id_produto')
	nome = TextField(db_column='nome_produto')
	tipo = TextField(db_column='tipo')
	template = TextField(db_column='template')


	@property
	def assunto(self):
		if (self.template.find('saude') != -1): 
  			return 'saude' 
		return 'seguros' 

	
	class Meta:
		table_name = 'clp_tb_produtos'

class Informe(BaseModel):
	id = PrimaryKeyField(db_column='id_informe')
	produto_id = IntegerField(db_column='id_produto')
	data = TextField(db_column='data')
	remetente = TextField(db_column='remetente')
	titulo = TextField(db_column='titulo')
	corpo = TextField(db_column='corpo')
	template = TextField(db_column='template')
	usuario_id = IntegerField(db_column='id_usuario')
	produto = ForeignKeyField(Produto, db_column='id_produto')
	
	class Meta:
		table_name = 'clp_tb_informes'

class InformeLog(BaseModel):
	informe_id = IntegerField(db_column='id_informe')
	cliente_id = IntegerField(db_column='id_cliente')
	status = TextField(db_column='status')
	tentativas = IntegerField(db_column='tentativas')
	cliente = ForeignKeyField(Cliente, db_column='id_cliente')
	informe = ForeignKeyField(Informe, db_column='id_informe')
	
	class Meta:
		primary_key = False
		table_name = 'clp_tb_informe_log'


def preparaEmail(corpo, Informe):
	if Informe.produto.tipo == 'I':
		if Informe.produto.template.find('saude') > 0:
			return secureProperties.INFORME_TEMPLATE.replace('#%#COR#%#', '#990033').replace('#%#CORPO#%#', corpo)
		return secureProperties.INFORME_TEMPLATE.replace('#%#COR#%#', '#009049').replace('#%#CORPO#%#', corpo)
		
#for cliente in Cliente.select():
	#print(cliente.nome_cliente)

#for informe in Informe.select():
#	print(informe.titulo, informe.remetente, informe.produto.nome_produto)

#for cliente in Cliente.select():
#	print('ID [{}] Nome [{}] Empresa[{}]'.format(cliente.id_cliente,cliente.nome_cliente, cliente.empresa.nome_empresa))
for informeLog in InformeLog.select().where((InformeLog.tentativas < 4) & (InformeLog.status == 'N')):
	if emailSend.send_single_email(informeLog.cliente.email, 
	html.unescape(informeLog.informe.titulo), 
	preparaEmail(html.unescape(informeLog.informe.corpo).replace('###','"'), informeLog.informe),
	informeLog.informe.template + '_t.jpg',
	'../images/' + informeLog.informe.template + '_t.jpg',
	'bottom_' + informeLog.informe.produto.assunto + '.jpg',
	'../images/bottom_' + informeLog.informe.produto.assunto + '.jpg'):
		print('email enviado')
		# atualizar o informe que foi enviado.
		InformeLog.update(status = 'S').where((InformeLog.informe_id == informeLog.informe_id) & (InformeLog.cliente_id == informeLog.cliente_id)).execute()
		InformeLog.update(tentativas = informeLog.tentativas + 1).where((InformeLog.informe_id == informeLog.informe_id) & (InformeLog.cliente_id == informeLog.cliente_id)).execute()
	else:
		print('email nao enviado')
		InformeLog.update(tentativas = informeLog.tentativas + 1).where((InformeLog.informe_id == informeLog.informe_id) & (InformeLog.cliente_id == informeLog.cliente_id)).execute()


