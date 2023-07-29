# Cadastro de Empresas - API

Este é um projeto de uma API para realizar operações CRUD (Create, Read, Update, Delete) em registros de empresas. A API foi desenvolvida em Python utilizando o framework Flask e Flask-RESTx para facilitar a criação de endpoints. Além disso, o SQLAlchemy foi utilizado para lidar com o banco de dados relacional e o Flask-Migrate para gerenciar as migrações do banco de dados.

## Configuração do Ambiente

Para executar o projeto localmente, você precisará ter o Python instalado em seu sistema.

Siga os passos abaixo para configurar o ambiente:

1. Clone o repositório:

```bash
git clone https://github.com/iuriaguiarr/estracta-test-python.git
cd estracta-test-python
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Executando o Projeto

Para executar o projeto, use o seguinte comando:

```bash
python app.py
```

O servidor local será iniciado e a API estará disponível no endereço `http://localhost:5000`.

## Testando os Endpoints

Para testar os endpoints da API, você pode utilizar uma ferramenta como o [Postman](https://www.postman.com/) ou utilizar o próprio Swagger gerado pelo Flask-RESTx.

1. Acesse a documentação da API através do Swagger:

Abra um navegador e navegue para `http://localhost:5000/`, onde você encontrará a documentação interativa da API. Lá você poderá visualizar todos os endpoints disponíveis, bem como os parâmetros necessários para cada operação.

2. Teste os Endpoints:

Você pode usar o Swagger para enviar solicitações para os endpoints e visualizar as respostas. Teste cada operação CRUD (Create, Read, Update, Delete) para verificar o funcionamento correto da API.

## Considerações Importantes

- A autenticação e autorização não foram implementadas.

- Os dados das empresas são armazenados no banco de dados SQLite.

- As validações de entrada são limitadas.

- Se você encontrar problemas ou tiver sugestões de melhoria, sinta-se à vontade para contribuir para o repositório do projeto.
