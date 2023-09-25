from flask import request, make_response, jsonify
from src.server.instance import server
from src.models.Endereco.Endereco import Endereco
from src.models.Endereco.Enderecos import Enderecos
from src.models.Erro import Erro
from flask_pydantic_spec import Response, Request
from db import conn

@server.app.get('/Enderecos')
# HTTP_200=Secoes
@server.api.validate(resp=Response(HTTP_200=Enderecos), tags=['Enderecos'])
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


@server.app.post('/Enderecos')
# HTTP_200=jsonify,
@server.api.validate(body=Request(Endereco), resp=Response(HTTP_400=Erro,  HTTP_500=Erro), tags=['Enderecos'])
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


@server.app.put('/Enderecos')
@server.api.validate(body=Request(Endereco), resp=Response(HTTP_400=Erro,  HTTP_500=Erro), tags=['Enderecos'])
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


@server.app.delete('/Enderecos')
@server.api.validate(body=Request(Endereco), resp=Response(HTTP_400=Erro,  HTTP_500=Erro), tags=['Enderecos'])
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


@server.app.post('/BuscarEnderecos')
# HTTP_200=Secoes
@server.api.validate(body=Request(Endereco), resp=Response(HTTP_200=Enderecos), tags=['Enderecos'])
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
            predicado += " and bairro like '%" + endereco['bairro'] + "%'"

    if (endereco.get("idCliente", False)):
        if (type(int(endereco['idCliente']) != int)) and (endereco['idCliente'] != 0) and (endereco['idCliente'] != ""):
            predicado += " and idCliente = " + str(endereco['idCliente']) + ""

    if (predicado == ""):
        predicado = " and id = 0"

    return predicado
