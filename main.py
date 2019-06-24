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
	nomeEmpresa = TextField(db_column='nome_empresa')
	razaoSocial = TextField(db_column='razao_social')
	endereco = TextField(db_column='endereco')
	cep = TextField(db_column='cep')
	cidade = TextField(db_column='cidade')
	estado = TextField(db_column='estado')
	telefone = TextField(db_column='telefone')
	fax = TextField(db_column='fax')
	observacao = TextField(db_column='observacao')
	contatoTitulo = TextField(db_column='contato_titulo')
	contatoNome = TextField(db_column='contato_nome')
	contatoCargo = TextField(db_column='contato_cargo')
	contatoTelefone = TextField(db_column='contato_telefone')
	contatoCelular = TextField(db_column='contato_celular')
	contatoEmail = TextField(db_column='contato_email')
	contatoFinanceiroTitulo = TextField(db_column='contato_financ_titulo')
	contatoFinanceiroNome = TextField(db_column='contato_financ_nome')
	contatoFinanceiroCargo = TextField(db_column='contato_financ_cargo')
	contatoFinanceiroTelefone = TextField(db_column='contato_financ_telefone')
	contatoFinanceiroCelular = TextField(db_column='contato_financ_celular')
	contatoFinanceiroEmail = TextField(db_column='contato_financ_email')
	tipoEnvio = IntegerField(default=0, db_column='tipo_envio')
	
	class Meta:
		table_name = 'clp_tb_empresas'
		
class Cliente(BaseModel):
	id = PrimaryKeyField(db_column='id_cliente')
	empresaId = IntegerField(db_column='id_empresa')
	nome = TextField(db_column='nome_cliente')
	titulo = TextField(db_column='titulo_cliente')
	cargo = TextField(db_column='cargo_cliente')
	dddFixo = TextField(db_column='dddf_cliente')
	fixo = TextField(db_column='telf_cliente')
	dddCelular = TextField(db_column='dddc_cliente')
	celular = TextField(db_column='telc_cliente')
	email = TextField(db_column='email_cliente')
	observacoes = TextField(db_column='observacoes_cliente')
	tipoEnvio = IntegerField(db_column='tipo_envio')
	habilitado = IntegerField(default=1, db_column='Habilitado')
	empresa = ForeignKeyField(Empresa, db_column='id_empresa')
	
	class Meta:
		table_name = 'clp_tb_clientes'

class Produto(BaseModel):
	id = PrimaryKeyField(db_column='id_produto')
	nome = TextField(db_column='nome_produto')
	tipo = TextField(db_column='tipo')
	template = TextField(db_column='template')
	
	class Meta:
		table_name = 'clp_tb_produtos'

class Informe(BaseModel):
	id = PrimaryKeyField(db_column='id_informe')
	produtoId = IntegerField(db_column='id_produto')
	data = TextField(db_column='data')
	remetente = TextField(db_column='remetente')
	titulo = TextField(db_column='titulo')
	corpo = TextField(db_column='corpo')
	template = TextField(db_column='template')
	usuarioId = IntegerField(db_column='id_usuario')
	produto = ForeignKeyField(Produto, db_column='id_produto')
	
	class Meta:
		table_name = 'clp_tb_informes'

class InformeLog(BaseModel):
	informeId = IntegerField(db_column='id_informe')
	clienteId = IntegerField(db_column='id_cliente')
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
	emailSend.send_single_email(informeLog.cliente.email, 
	html.unescape(informeLog.informe.titulo), 
	preparaEmail(html.unescape(informeLog.informe.corpo).replace('###','"'), informeLog.informe)
	)
	print(html.unescape(informeLog.informe.remetente))
	print(informeLog.cliente.email)
	print(html.unescape(informeLog.informe.titulo))
	print(preparaEmail(html.unescape(informeLog.informe.corpo).replace('###','"'), informeLog.informe))


