from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


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

@app.route('/ingredientes', methods = ['GET'])
def ingredientes():
    '''
    Devuelve el nombre e ingredientes de los platos para poder armar la lista de compra
    '''
    conn = engine.connect() # Creamos la conexión con la base de datos
    query = "SELECT nombre, ingredientes FROM recetas;" # Generamos la query para obtener los nombres e ingredientes de las recetas

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
    conn = engine.connect() # Creamos la conexión con la base de datos
    query = f"SELECT password FROM usuarios WHERE username = '{username}';" # Generamos la query para obtener la contraseña del usuario


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



if __name__ == "__main__":
    app.run("127.0.0.1", port="5000", debug=True)