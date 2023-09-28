from flask import Flask, make_response, jsonify, request
from flask_pydantic_spec import FlaskPydanticSpec
from flask_pydantic_spec import Response, Request
import psycopg2
from src.models.Endereco.Endereco import Endereco
from src.models.Endereco.Enderecos import Enderecos
from src.models.Cliente.Cliente import Cliente
from src.models.Cliente.Clientes import Clientes
from src.models.Erro import Erro
from flask_cors import CORS

app = Flask(__name__)
spec = FlaskPydanticSpec()
spec.register(app)
CORS(app)

# conn = psycopg2.connect(database="clientes",
#                        user="postgres",
#                        password="123456",
#                        host="localhost", port="5432")

conn = psycopg2.connect(database="clientes",
                        user="postgres",
                        password="123456",
                        host="bd_postgres_clientes")


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


@app.put('/Cliente')
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


@app.delete('/Cliente')
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
        sqlEndereco = f"DELETE FROM ENDERECOS WHERE IDCLIENTE = {cliente['id']}"
        cursor.execute(sqlEndereco)
        cursor.execute(sql)

        conn.commit()

        cursor.close()
        return make_response(
            jsonify(body))

    except Exception as e:
        return make_response(
            jsonify(Erro(status=500, msg="Não é possível excluir.").dict())), 500


@app.post('/BuscarCliente')
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
            predicado += " and LOWER(nome) like '%" + \
                str(cliente['nome']).lower() + "%'"

    if (cliente.get("id", False)):
        if (type(int(cliente['id']) != int)) and (cliente['id'] != 0) and (cliente['id'] != ""):
            predicado += " and id = " + str(cliente['id']) + ""

    if (cliente.get("documento", False)):
        if (cliente['documento'] != "") and (len(cliente['documento']) == 11):
            predicado += " and documento like '%" + cliente['documento'] + "%'"

    if (predicado == ""):
        predicado = " and id = 0"

    return predicado


@app.get('/Endereco')
# HTTP_200=Secoes
@spec.validate(resp=Response(HTTP_200=Enderecos), tags=['Enderecos'])
def GetEnderecos():
    """
    Retorna todos os clientes ativos da base de dados

    """
    cursor = conn.cursor()
    cursor.execute(
        'SELECT id, logradouro, bairro, cep, numero, complemento, cidade, idCliente, estado FROM enderecos Where ativa = true')
    enderecos = cursor.fetchall()
    cursor.close()

    enderecosVO = list()
    for ed in enderecos:
        enderecosVO.append({
            'id': ed[0],
            'logradouro': ed[1],
            'bairro': ed[2],
            'cep': ed[3],
            'numero': ed[4],
            'complemento': ed[5],
            'cidade': ed[6],
            'estado': ed[8],
            'idCliente': ed[7]
        })

    return make_response(
        jsonify(Enderecos(Enderecos=enderecosVO).dict()))


@app.post('/Endereco')
# HTTP_200=jsonify,
@spec.validate(body=Request(Endereco), resp=Response(HTTP_400=Erro,  HTTP_500=Erro), tags=['Enderecos'])
def PostEnderecos():
    """
    Insere um endereco da base de dados

    """
    try:
        body = request.context.body.dict()
        endereco = request.json

        if (endereco['bairro'] != "") and (endereco['cep'] != "") and (endereco['cidade'] != "") and (endereco['estado'] != "") and (endereco['idCliente'] != "") and (endereco['logradouro'] != "") and (endereco['numero'] != ""):

            # verificar se cliente existe usando o id

            cursor = conn.cursor()
            sql = f"INSERT INTO ENDERECOS(bairro, cep, cidade, complemento, estado, idCliente, logradouro, numero) VALUES('{endereco['bairro']}', '{endereco['cep']}', '{endereco['cidade']}', '{endereco['complemento']}', '{endereco['estado']}', '{endereco['idCliente']}', '{endereco['logradouro']}', '{endereco['numero']}')"
            cursor.execute(sql)
            conn.commit()
            cursor.close()
            return body

        return make_response(
            jsonify(Erro(status=400, msg="Não foi possível incluir o endereco. Verifique os parêmetros enviados").dict())), 400

    except Exception as e:
        return make_response(
            jsonify(Erro(status=500, msg="Houve um erro grave com a aplicação").dict())), 500


@app.put('/Endereco')
@spec.validate(body=Request(Endereco), resp=Response(HTTP_400=Erro,  HTTP_500=Erro), tags=['Enderecos'])
def PutEnderecos():
    """
    Atualiza o endereco da base de dados de clientes

    """
    try:

        body = request.context.body.dict()
        endereco = request.json
        query = ""

        if (endereco.get("bairro", False)):
            if (endereco['bairro'] == "") or (len(endereco['bairro']) < 3):
                return make_response(
                    jsonify(Erro(status=400, msg="Não é possível atualizar o bairro. Verifique os parêmetros enviados").dict())), 400
            else:
                if (len(query) > 0):
                    query += ","

                query += " bairro = '" + endereco['bairro'] + "'"

        if (endereco.get("cep", False)):
            if (endereco['cep'] == "") or (len(endereco['cep']) < 8):
                return make_response(
                    jsonify(Erro(status=400, msg="Não é possível atualizar o cep. Verifique os parêmetros enviados").dict())), 400
            else:
                if (len(query) > 0):
                    query += ","
                query += " cep = '" + endereco['cep'] + "'"

        if (endereco.get("cidade", False)):
            if (endereco['cidade'] == "") or (len(endereco['cidade']) < 2):
                return make_response(
                    jsonify(Erro(status=400, msg="Não é possível atualizar a cidade. Verifique os parêmetros enviados").dict())), 400
            else:
                if (len(query) > 0):
                    query += ","
                query += " cidade = '" + endereco['cidade'] + "'"

        if (endereco.get("estado", False)):
            if (endereco['estado'] == "") or (len(endereco['estado']) < 2):
                return make_response(
                    jsonify(Erro(status=400, msg="Não é possível atualizar o estado. Verifique os parêmetros enviados").dict())), 400
            else:
                if (len(query) > 0):
                    query += ","
                query += " estado = '" + endereco['estado'] + "'"

        if (endereco.get("logradouro", False)):
            if (endereco['logradouro'] == "") or (len(endereco['logradouro']) < 2):
                return make_response(
                    jsonify(Erro(status=400, msg="Não é possível atualizar o logradouro. Verifique os parêmetros enviados").dict())), 400
            else:
                if (len(query) > 0):
                    query += ","
                query += " logradouro = '" + endereco['logradouro'] + "'"

        if (endereco.get("numero", False)):
            if (endereco['numero'] == "") or (type(int(endereco['numero'])) != int):
                return make_response(
                    jsonify(Erro(status=400, msg="Não é possível atualizar o número do endereço. Verifique os parêmetros enviados").dict())), 400
            else:
                if (len(query) > 0):
                    query += ","
                query += " numero = '" + endereco['numero'] + "'"

        if (endereco.get("id", False)):
            if (endereco['id'] == "") or (type(int(endereco['id'])) != int) or (endereco['id'] == 0):
                return make_response(
                    jsonify(Erro(status=400, msg="Não é possível atualizar o endereço pois o id do mesmo não foi informado ou é igual a 0. Verifique os parêmetros enviados").dict())), 400
        else:
            if (endereco['id'] == "") or (type(int(endereco['id'])) != int) or (endereco['id'] == 0):
                return make_response(
                    jsonify(Erro(status=400, msg="Não é possível atualizar o endereço pois o id do mesmo não foi informado ou é igual a 0. Verifique os parêmetros enviados").dict())), 400

        if (endereco.get("idCliente", False)):
            if (endereco['idCliente'] == "") or (type(int(endereco['idCliente'])) != int) or (endereco['idCliente'] == 0):
                return make_response(
                    jsonify(Erro(status=400, msg="Não é possível atualizar o endereço pois o cliente do mesmo não foi informado ou é igual a 0. Verifique os parêmetros enviados").dict())), 400
        else:
            if (endereco['idCliente'] == "") or (type(int(endereco['idCliente'])) != int) or (endereco['idCliente'] == 0):
                return make_response(
                    jsonify(Erro(status=400, msg="Não é possível atualizar o endereço pois o id do mesmo não foi informado ou é igual a 0. Verifique os parêmetros enviados").dict())), 400

        if (endereco.get("complemento", False)):
            if (len(query) > 0):
                query += ","
            query += " complemento = '" + endereco['complemento'] + "'"

        cursor = conn.cursor()
        sql = f"UPDATE ENDERECOS SET {query} WHERE ID = {endereco['id']} AND IDCLIENTE = {endereco['idCliente']}"
        cursor.execute(sql)
        conn.commit()
        cursor.close()

        return make_response(
            jsonify(body))

    except Exception as e:
        return make_response(
            jsonify(Erro(status=500, msg="Houve um erro durante a atualização").dict())), 500


@app.delete('/Endereco')
@spec.validate(body=Request(Endereco), resp=Response(HTTP_400=Erro,  HTTP_500=Erro), tags=['Enderecos'])
def DeleteEnderecos():
    """
    Deleta um endereco da base de dados

    """
    try:
        body = request.context.body.dict()
        endereco = request.json
        # clientes = retorna_produtos(secao['id'])

        if (endereco['id'] == "") or (endereco['id'] == "0") or (type(int(endereco['id'])) != int):
            return make_response(
                jsonify(Erro(status=400, msg="Id do endereco não especificado. Verifique os parêmetros enviados").dict())), 400

        cursor = conn.cursor()
        sql = f"DELETE FROM ENDERECOS WHERE ID = {endereco['id']}"
        cursor.execute(sql)
        conn.commit()

        cursor.close()
        return make_response(
            jsonify(body))

    except Exception as e:
        return make_response(
            jsonify(Erro(status=500, msg="Não é possível excluir.").dict())), 500


@app.post('/BuscarEndereco')
# HTTP_200=Secoes
@spec.validate(body=Request(Endereco), resp=Response(HTTP_200=Enderecos), tags=['Enderecos'])
def BuscarEndereco():
    """
    Retorna um endereco de acordo com os parâmetros pesquisados

    """

    cursor = conn.cursor()
    cursor.execute('SELECT id, logradouro, bairro, cep, numero, complemento, cidade, idCliente, estado FROM ENDERECOS Where ativa = true ' +
                   MontaPredicadoBuscaEnderecos(request))
    enderecos = cursor.fetchall()
    cursor.close()

    enderecosVO = list()
    for ed in enderecos:
        enderecosVO.append({
            'id': ed[0],
            'logradouro': ed[1],
            'bairro': ed[2],
            'cep': ed[3],
            'numero': ed[4],
            'complemento': ed[5],
            'cidade': ed[6],
            'estado': ed[8],
            'idCliente': ed[7]
        })

    return make_response(
        jsonify(Enderecos(Enderecos=enderecosVO).dict()))


def MontaPredicadoBuscaEnderecos(Enderecos):
    endereco = Enderecos.json
    predicado = ""

    if (endereco.get("bairro", False)):
        if (endereco['bairro'] != "") and (len(endereco['bairro']) > 2):
            predicado += " and LOWER(bairro) like '%" + \
                str(endereco['bairro']).lower() + "%'"

    if (endereco.get("idCliente", False)):
        if (type(int(endereco['idCliente']) != int)) and (endereco['idCliente'] != 0) and (endereco['idCliente'] != ""):
            predicado += " and idCliente = " + str(endereco['idCliente']) + ""

    if (predicado == ""):
        predicado = " and id = 0"

    return predicado


app.run()

# from src.server.instance import server
# from src.controllers.clientes import Clientes
# from src.controllers.endereco import Enderecos

# server.run()
