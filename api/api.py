from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


app = Flask(__name__)

# Parametros de conexion
USUARIO = "root"
CONTRASEÑA = "lanzillotta"
HOST = "localhost"
DATABASE = "introds"


URI = f"mysql+mysqlconnector://{USUARIO}:{CONTRASEÑA}@{HOST}/{DATABASE}"

engine = create_engine(URI)


@app.route('/platos', methods = ['GET'])
def platos():
    conn = engine.connect()
    
    query = "SELECT * FROM test;"
    try:
        #Se debe usar text para poder adecuarla al execute de mysql-connector
        result = conn.execute(text(query))
        #Se hace commit de la consulta (acá no estoy seguro si es necesario para un select, sí es necesario para un insert!)
        conn.close() #Cerramos la conexion con la base de datos
    except SQLAlchemyError as err:
        return jsonify(str(err.__cause__))
    
    #Se preparan los datos para ser mostrador como json
    data = []
    for row in result:
        entity = {}
        entity['id'] = row.id
        entity['plato'] = row.plato
        entity['ingredientes'] = row.ingredientes
        entity['creado'] = row.creado
        entity['dueño'] = row.dueño
        data.append(entity)

    return jsonify(data), 200

if __name__ == "__main__":
    app.run("127.0.0.1", port="5000", debug=True)