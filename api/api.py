from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import json


app = Flask(__name__)

# Parametros de conexion
USUARIO = "root"
CONTRASEÑA = "codigofiuba"
HOST = "localhost"
DATABASE = "tp_ids"

# URI (Uniform Resource Identifier) para conectar con la databse
URI = f"mysql+mysqlconnector://{USUARIO}:{CONTRASEÑA}@{HOST}/{DATABASE}"

# Funcion para conectarse a la base de datos
engine = create_engine(URI)


@app.route('/platos', methods = ['GET'])
def platos():
    '''
    Devuelve el nombre y descripcion de los platos para poder ser mostrados en el template del menu
    '''
    conn = engine.connect() # Creamos la conexión con la base de datos
    query = "SELECT nombre, descripcion FROM recetas;" # Generamos la query para obtener los nombres y descripciones de las recetas

    try:
        result = conn.execute(text(query)) # Usamos text para poder usar un string como query y que execute la interprete
        conn.close() #Cerramos la conexion con la base de datos

    except SQLAlchemyError as err: # Agarramos cualquier excepcion que SQLAlchemy pueda tener
        return jsonify(str(err.__cause__)), 500
    
    data = [] # Armamos una lista para agregar diccionarios con todos los datos
    for row in result: # Recorremos las lineas del resultado de la query
        entity = {}
        entity['nombre'] = row.nombre
        entity['descripcion'] = row.descripcion
        data.append(entity)

    return jsonify(data), 200 # Devolvemos la informacion obtenida


@app.route('/ingredientes/<lista_platos>', methods = ['GET'])
def ingredientes(lista_platos):
    '''
    Devuelve el nombre e ingredientes de los platos para poder armar la lista de compra
    PRECONDICION: lista_platos es una tupla de nombres de comidas
    '''
    conn = engine.connect() # Creamos la conexión con la base de datos
    query = f"SELECT ingredientes FROM recetas WHERE nombre in {lista_platos};" # Generamos la query para obtener los nombres e ingredientes de las recetas

    try:
        result = conn.execute(text(query)) # Usamos text para poder usar un string como query y que execute la interprete
        conn.close() #Cerramos la conexion con la base de datos

    except SQLAlchemyError as err: # Agarramos cualquier excepcion que SQLAlchemy pueda tener
        return jsonify(str(err.__cause__)), 500
    
    data = [] # Armamos una lista para agregar diccionarios con todos los datos
    for row in result: # Recorremos las lineas del resultado de la query
        entity = {}
        entity['ingredientes'] = row.ingredientes
        data.append(entity)

    return jsonify(data), 200 # Devolvemos la informacion obtenida


@app.route('/login/<username>', methods = ['GET'])
def get_password(username):
    '''Devuelve la contraseña del usuario pasado por la ruta en formato de string.
    En caso de que el usuario no exista en la base de datos devuelve una cadena vacia'''
   
    conn = engine.connect()
    query = f"SELECT password FROM usuarios WHERE username = '{username}';"

    try:
        result = conn.execute(text(query)) # Usamos text para poder usar un string como query y que execute la interprete
        row = result.fetchone() # Obtenemos solo 1 fila, porque los usuarios son unicos en la database
        conn.close() #Cerramos la conexion con la base de datos

    except SQLAlchemyError as err: # Agarramos cualquier excepcion que SQLAlchemy pueda tener
        return jsonify(str(err.__cause__)), 500
    
    if not row:
        return jsonify(""), 200 # Si el usuario no existe, devuelve una cadena vacia

    else:
        return jsonify(row[0]), 200 # Devuelvo un json con el primer (y unico) elemento de la row que es la password


@app.route('/crear_receta', methods = ['POST'])
def crear_receta():
    conn = engine.connect()
    receta = request.get_json()

    json_ingredientes = json.dumps(receta['ingredientes'])  #Se maneja automaticamante el formato JSON para espaciar caracteres especiales

    #Se crea la query en base a los datos pasados por el endpoint.
    #Los mismos deben viajar en el body en formato JSON raw
    query = f"""INSERT INTO recetas (nombre, ingredientes, duenio, descripcion) 
    VALUES ('{receta['nombre']}',
            '{json_ingredientes}',
            '{receta["duenio"]}',
            '{receta["descripcion"]}'
            );"""
    
    try:
        result = conn.execute(text(query))    # Se ejecuta la query
        conn.commit()   # Se aplica a la base de datos
        conn.close()      # Se cierra la conexion con la database
    except SQLAlchemyError as err:
        return jsonify({'message': 'Se ha producido un error' + str(err.__cause__)}), 500
    
    return jsonify({'message': 'se ha agregado correctamente' + query}), 201


@app.route('/borrar_receta/<nombre>', methods = ['DELETE'])
def borrar_receta(nombre):
    conn = engine.connect()
    query = f"DELETE FROM recetas WHERE nombre = {nombre}" # query para borrar
    validation_query = f"SELECT * FROM recetas WHERE nombre = {nombre}" # query para verificar que el plato exista
    print(query, validation_query)
    
    try:
        val_result = conn.execute(text(validation_query))
        if val_result.rowcount != 0 :
            result = conn.execute(text(query))
            conn.commit()
            conn.close()
        else:
            conn.close()
            return jsonify({"message": "El plato no existe"}), 404
    
    except SQLAlchemyError as err:
        return jsonify({'message': 'Se ha producido un error' + str(err.__cause__)}), 500
    
    return jsonify({'message': 'se ha eliminado correctamente'}), 202


if __name__ == "__main__":
    app.run("127.0.0.1", port="5000", debug=True)