from flask import Flask, make_response, jsonify, request
from flask_pydantic_spec import FlaskPydanticSpec
from flask_pydantic_spec import Response, Request
import psycopg2
from src.models.Secao.Secao import Secao
from src.models.Secao.Secoes import Secoes
from src.models.Cliente.Cliente import Cliente
from src.models.Cliente.Clientes import Clientes
from src.models.Erro import Erro
from flask_cors import CORS

app = Flask(__name__)
spec = FlaskPydanticSpec()
spec.register(app)
CORS(app)

conn = psycopg2.connect(database="clientes",
                        user="postgres",
                        password="123456",
                        host="localhost", port="5432")

# conn = psycopg2.connect(database="clientes",
#            user="postgres",
#            password="123456",
#           host="bd_postgres_clientes")


@app.get('/Cliente')
# HTTP_200=Secoes
@spec.validate(resp=Response(HTTP_200=Clientes), tags=['Clientes'])
def Get():
    """
    Retorna todos os clientes ativos da base de dados

    """
    cursor = conn.cursor()
    cursor.execute(
        'SELECT id, nome, documento FROM clientes Where ativo = true')
    clientes = cursor.fetchall()
    cursor.close()

    clientesVO = list()
    for sc in clientes:
        clientesVO.append({
            'id': sc[0],
            'nome': sc[1],
            'documento': sc[2]
        })

    return make_response(
        jsonify(Clientes(Clientes=clientesVO).dict()))


@app.post('/Cliente')
# HTTP_200=jsonify,
@spec.validate(body=Request(Cliente), resp=Response(HTTP_400=Erro,  HTTP_500=Erro), tags=['Clientes'])
def Post():
    """
    Insere um cliente da base de dados

    """
    try:
        body = request.context.body.dict()
        cliente = request.json

        if (cliente['nome'] != "") and (cliente['documento'] != ""):
            cursor = conn.cursor()
            sql = f"INSERT INTO CLIENTES(NOME, DOCUMENTO) VALUES('{cliente['nome']}', '{cliente['documento']}')"
            cursor.execute(sql)
            conn.commit()
            cursor.close()
            return body

        return make_response(
            jsonify(Erro(status=400, msg="Não foi possível incluir o cliente. Verifique os parêmetros enviados").dict())), 400

    except Exception as e:
        return make_response(
            jsonify(Erro(status=500, msg="Houve um erro grave com a aplicação").dict())), 500


@app.put('/Clientes')
@spec.validate(body=Request(Cliente), resp=Response(HTTP_400=Erro,  HTTP_500=Erro), tags=['Clientes'])
def Put():
    """
    Atualiza a seção da base de dados de clientes

    """
    try:

        body = request.context.body.dict()
        cliente = request.json

        if cliente['nome'] == "":
            return make_response(
                jsonify(Erro(status=400, msg="Não é possível atualizar o nome do cliente. Verifique os parêmetros enviados").dict())), 400

        if len(cliente['nome']) < 3:
            return make_response(
                jsonify(Erro(status=400, msg="Nome do cliente deve ter mais de 2 caracteres. Verifique os parêmetros enviados").dict())), 400

        if cliente['id'] == "":
            return make_response(
                jsonify(Erro(status=400, msg="Id do cliente não especificado. Verifique os parêmetros enviados").dict())), 400

        if cliente['id'] == 0:
            return make_response(
                jsonify(Erro(status=400, msg="Id do cliente não especificado. Verifique os parêmetros enviados").dict())), 400

        if type(int(cliente['id'])) != int:
            return make_response(
                jsonify(Erro(status=400, msg="Id do cliente inválido. Verifique os parêmetros enviados").dict())), 400

        cursor = conn.cursor()
        sql = f"UPDATE CLIENTES SET NOME = '{cliente['nome']}' WHERE ID = {cliente['id']}"
        cursor.execute(sql)
        conn.commit()
        cursor.close()

        return make_response(
            jsonify(body))

    except Exception as e:
        return make_response(
            jsonify(Erro(status=500, msg="Houve um erro durante a atualização").dict())), 500


@app.delete('/Clientes')
@spec.validate(body=Request(Cliente), resp=Response(HTTP_400=Erro,  HTTP_500=Erro), tags=['Clientes'])
def Delete():
    """
    Deleta um cliente da base de dados

    """
    try:
        body = request.context.body.dict()
        cliente = request.json
        # clientes = retorna_produtos(secao['id'])

        if cliente['id'] == "":
            return make_response(
                jsonify(Erro(status=400, msg="Id do cliente não especificado. Verifique os parêmetros enviados").dict())), 400

        if cliente['id'] == "0":
            return make_response(
                jsonify(Erro(status=400, msg="Id do cliente não especificado. Verifique os parêmetros enviados").dict())), 400

        if type(int(cliente['id'])) != int:
            return make_response(
                jsonify(Erro(status=400, msg="Id da Seção inválido. Verifique os parêmetros enviados").dict())), 400

        # if  clientes > 0:
         #   return make_response(
          #      jsonify(Erro(status=400, msg="Não é possível excluir pois existem produtos vinculados").dict())), 400

        cursor = conn.cursor()
        sql = f"DELETE FROM CLIENTES WHERE ID = {cliente['id']}"
        cursor.execute(sql)
        conn.commit()

        cursor.close()
        return make_response(
            jsonify(body))

    except Exception as e:
        return make_response(
            jsonify(Erro(status=500, msg="Não é possível excluir.").dict())), 500


@app.post('/BuscarClientes')
# HTTP_200=Secoes
@spec.validate(body=Request(Cliente), resp=Response(HTTP_200=Clientes), tags=['Clientes'])
def BuscarCliente():
    """
    Retorna um cliente de acordo com os parâmetros pesquisados

    """

    cursor = conn.cursor()
    cursor.execute('SELECT id, nome, documento FROM CLIENTES Where ativo = true ' +
                   MontaPredicadoBuscaCliente(request))
    clientes = cursor.fetchall()
    cursor.close()

    clientesVO = list()
    for sc in clientes:
        clientesVO.append({
            'id': sc[0],
            'nome': sc[1],
            'documento': sc[2]
        })

    return make_response(
        jsonify(Clientes(Clientes=clientesVO).dict()))


def MontaPredicadoBuscaCliente(Clientes):
    cliente = Clientes.json
    predicado = ""

    if (cliente.get("nome", False)):
        if (cliente['nome'] != "") and (len(cliente['nome']) > 2):
            predicado += " and nome like '%" + cliente['nome'] + "%'"

    if (cliente.get("id", False)):
        if (type(int(cliente['id']) != int)) and (cliente['id'] != 0) and (cliente['id'] != ""):
            predicado += " and id = " + str(cliente['id']) + ""

    if (cliente.get("documento", False)):
        if (cliente['documento'] != "") and (len(cliente['documento']) == 11):
            predicado += " and documento like '%" + cliente['documento'] + "%'"

    if (predicado == ""):
        predicado = " and id = 0"

    return predicado


app.run()
