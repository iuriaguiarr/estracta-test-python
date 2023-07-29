from flask import Flask, request
from flask_restx import Api, Resource, fields
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.inspection import inspect 


app = Flask(__name__)
api = Api(app)

# Configuração do SQLite
engine = create_engine('sqlite:///database.db')
Base = declarative_base()

# Companies table model
class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    cnpj = Column(String(14), unique=True, nullable=False)
    name_legal_entity = Column(String(100), nullable=False)
    trade_name = Column(String(100), nullable=False)
    cnae = Column(String(10), nullable=False)

# Checa se a tabela existe. Caso não exista, cria
if not inspect(engine).has_table('companies'):
    Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


# Definição de Namespace para os endpoints
company_ns = api.namespace('companies', description='Operations related to companies')

# Definição de modelo para o Swagger
company_model = api.model('Company', {
    'cnpj': fields.String(required=True, description='Company CNPJ'),
    'name_legal_entity': fields.String(required=True, description='Company Legal Name'),
    'trade_name': fields.String(required=True, description='Company Trade Name'),
    'cnae': fields.String(required=True, description='Company CNAE')
})

# Endpoint para criar uma empresa
@company_ns.route('/register/')
class RegisterCompany(Resource):
    @company_ns.expect(company_model, validate=True)
    @company_ns.response(201, 'Company successfully registered')
    def post(self):
        parser = api.parser()
        parser.add_argument('cnpj', type=str, required=True)
        parser.add_argument('name_legal_entity', type=str, required=True)
        parser.add_argument('trade_name', type=str, required=True)
        parser.add_argument('cnae', type=str, required=True)
        args = parser.parse_args()

        session = Session()
        company = Company(
            cnpj=args['cnpj'],
            name_legal_entity=args['name_legal_entity'],
            trade_name=args['trade_name'],
            cnae=args['cnae']
        )
        session.add(company)
        session.commit()
        session.close()

        return {'message': 'Company successfully registered'}, 201

# Endpoint para editar uma empresa
@company_ns.route('/edit/<string:cnpj>')
class EditCompany(Resource):
    @company_ns.expect(company_model, validate=True)
    @company_ns.response(200, 'Company successfully updated')
    def put(self, cnpj):
        parser = api.parser()
        parser.add_argument('trade_name', type=str, required=True)
        parser.add_argument('cnae', type=str, required=True)
        args = parser.parse_args()

        session = Session()
        company = session.query(Company).filter_by(cnpj=cnpj).first()
        if not company:
            return {'message': 'Company not found'}, 404

        # Atualizando os campos
        company.trade_name = args['trade_name']
        company.cnae = args['cnae']

        session.commit()
        session.close()

        return {'message': 'Company successfully updated'}

# Endpoint para remover uma empresa
@company_ns.route('/delete/<string:cnpj>')
class RemoveCompany(Resource):
    @company_ns.response(404, 'Company not found')
    @company_ns.response(200, 'Company successfully removed')
    def delete(self, cnpj):
        session = Session()
        company = session.query(Company).filter_by(cnpj=cnpj).first()
        if not company:
            return {'message': 'Company not found'}, 404

        session.delete(company)
        session.commit()
        session.close()

        return {'message': 'Company successfully removed'}

# Endpoint para listar as empresas
@company_ns.route('/list')
class ListCompanies(Resource):
    @company_ns.response(200, 'List of companies')
    def get(self):
        start = int(request.args.get('start', 0))
        limit = int(request.args.get('limit', 10))
        sort = request.args.get('sort', 'trade_name')
        dir = request.args.get('dir', 'asc')

        session = Session()
        query = session.query(Company)

        # Ordenando
        if dir == 'asc':
            query = query.order_by(getattr(Company, sort).asc())
        else:
            query = query.order_by(getattr(Company, sort).desc())

        # Paginando
        companies = query.offset(start).limit(limit).all()

        session.close()

        # Convertendo a lista para um retorno em JSON
        companies_list = []
        for company in companies:
            companies_list.append({
                'id': company.id,
                'cnpj': company.cnpj,
                'name_legal_entity': company.name_legal_entity,
                'trade_name': company.trade_name,
                'cnae': company.cnae
            })

        return {'companies': companies_list, 'total': len(companies_list)}


api.add_resource(RegisterCompany, '/companies/register')
api.add_resource(EditCompany, '/companies/edit/<string:cnpj>')
api.add_resource(RemoveCompany, '/companies/delete/<string:cnpj>')
api.add_resource(ListCompanies, '/companies')

if __name__ == '__main__':
    app.run(debug=True)
