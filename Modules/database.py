from shutil import register_unpack_format
import mysql.connector

def getConnection():
  return mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    database = 'simulado'
  )

def getAreas():
  result = []

  conn = getConnection()

  cursor = conn.cursor()

  query = """
    SELECT area, sum(quantidade) 
    FROM Alocacao 
    GROUP BY area 
    ORDER BY area
  """
  
  cursor.execute(query)
  resultTable = cursor.fetchall()

  for row in resultTable:
    result.append({ 'id': row[0], 'quantidade': row[1] })

  conn.close()

  return result

def getVeiculosPorArea(idArea):
  result = []

  conn = getConnection()

  cursor = conn.cursor()

  query = """
    SELECT Veiculos.id, Veiculos.modelo, Veiculos.preco
    FROM Veiculos
    WHERE id IN 
      (SELECT id_veiculo 
        FROM Alocacao 
        WHERE area = %(area)s and quantidade > 0)
  """.format(idArea)

  params = { 'area': idArea}

  cursor.execute(query, params)
  data = cursor.fetchall()

  for row in data: 
    result.append({ 'id': row[0], 'modelo': row[1], 'preco': row[2] })

  conn.close()
  
  return result

def getVeiculoPorId(idVeiculo):
  result = None

  conn = getConnection()

  cursor = conn.cursor()

  query = """
    SELECT id, modelo, preco
    FROM Veiculos
    WHERE id = %(id)s
  """

  params = { 'id': idVeiculo }

  cursor.execute(query, params)
  data = cursor.fetchone()

  if data:
    result = {'id': data[0], 'modelo': data[1], 'preco':  data[2]}

  conn.close()
  
  return result

def getClientes():
  result = []

  conn = getConnection()

  cursor = conn.cursor()

  query = """
    SELECT *
    FROM Clientes
  """

  cursor.execute(query)
  data = cursor.fetchall()

  if data:
    for row in data:
      result.append({'id': row[0], 'nome':row[1]})
    
  conn.close()

  return result

def getConcessionarias():
  result = []

  conn = getConnection()

  cursor = conn.cursor()

  query = """
    SELECT *
    FROM Concessionarias
  """

  cursor.execute(query)
  data = cursor.fetchall()

  if data:
    for row in data:
      result.append({'id': row[0], 'nome':row[1]})
    
  conn.close()

  return result

def insertVenda(idVeiculo, idCliente, idConcessionaria, idArea):
  conn = getConnection()

  cursor = conn.cursor()

  query = """
    INSERT INTO VENDAS (id_cliente, id_veiculo, id_concessionaria)
    VALUES (%(cliente)s, %(veiculo)s, %(concessionaria)s);
  """

  params = {
    'cliente': idCliente,
    'veiculo': idVeiculo,
    'concessionaria': idConcessionaria,
  }

  cursor.execute(query, params)
  conn.commit()

  query = """
    UPDATE Alocacao
    SET quantidade = quantidade - 1
    WHERE area = %(area)s AND id_veiculo = %(veiculo)s
  """

  params = {
    'veiculo': idVeiculo,
    'area': idArea
  }

  cursor.execute(query, params)
  conn.commit()

  conn.close()