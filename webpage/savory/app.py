from flask import Flask, request, render_template, redirect, url_for, send_from_directory, session
import requests
import os
from base64 import b64decode


app = Flask(__name__)
app.secret_key = os.urandom(15)       # La secret_key es necesaria para validar sesiones de usuarios

def cant_ingredientes(list_dicc):
    ingredientes = {} 
    for i in range(len(list_dicc)):
        for ingrediente, cantidad in list_dicc[i].items():
            ingredientes[ingrediente] = ingredientes.get(ingrediente, "") + cantidad
    return ingredientes

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/favicon.ico")
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico',mimetype='image/vnd.microsof.icon')


@app.route('/menu')
def menu():
    api_url = f'http://127.0.0.1:5000/platos'
    response = requests.get(api_url)
    lista_platos = response.json()       # Nombre y descripcion de los platos de la database

    return render_template('menu.html', platosjson=lista_platos)

@app.route("/seleccion", methods=["GET", "POST"])
def seleccion():
    lista_recetas = ["Hamburgesa", "Sopa de tomate", "Mate"] 

    if request.method == "POST":
        recetas_elegidas = request.form.getlist("recetas")      #Recibe las recetas seleccionadas en los checkbox
        api_url = f'http://127.0.0.1:5000/ingredientes/{tuple(recetas_elegidas)}'       # Devuelve nombre e ingredientes de cada plato
        response = requests.get(api_url)
        json_ingredientes_desarmado = response.json()
        json_ingredientes_ordenado = cant_ingredientes(json_ingredientes_desarmado)     # Ordena las cantidades y unidades del diccionario de ingredientes

        return redirect(url_for('listado',json_ingredientes = json_ingredientes_ordenado))
    
    return render_template("lista_recetas.html", lista_recetas=lista_recetas)

@app.route("/listado")
def listado():
    json_ingredientes = request.args.get('json_ingredientes')
    return render_template("lista_compra.html",dicc=json_ingredientes)
    #mostrar la lista de la compra


@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        username_form = request.form.get('username_form')
        password_form = request.form.get('password_form')

        # Realiza la solicitud a la API de backend
        api_url = f'http://127.0.0.1:5000/login/{username_form}'
        response = requests.get(api_url)
        response_str = response.json()  # Contraseña asignada al usuario en la database

        assigned_password_bytes = b64decode(response_str)  # Decodificacion a bytes
        assigned_password = assigned_password_bytes.decode("utf-8")  # Casteo de bytes a str

        if password_form == assigned_password:
            session['auth'] = True                  # Autentica la sesion del usuario
            session['user'] = username_form          # Asigna el username autenticado en la sesion
            return redirect(url_for('suggest'))

    return render_template('login.html')


@app.route('/suggest', methods=["GET","POST"])
def suggest():
    if not session.get('auth'):
        return redirect(url_for('login'))

    if request.method == "POST":         #Si es metodo post(ya se completo el primer form), guarda la cantidad de campos a usar
        cantidad = int(request.form.get("numIngredientes"))
        nombre = request.form.get("namePlato")      #Estos 2 datos tienen que ser enviados a la api pra meterlos en la BBDD
        descripcion = request.form.get("descPlato")
        return redirect(url_for('suggest_ingredientes', cantidad=cantidad, nombre=nombre, descripcion=descripcion))    #Redirecciona a el forms de ingredientes, pasando la cantidad de camposcl

    return render_template("form_receta.html", username=session.get('user'))


@app.route('/suggest/ingredientes', methods=["GET","POST"])
def suggest_ingredientes():
    if not session.get('auth'):
        return redirect(url_for('login'))

    cantidad = int(request.args.get('cantidad'))   #Recibe cantidad como argumento
    nombre = str(request.args.get('nombre'))
    descripcion = str(request.args.get('descripcion'))

    duenio = session.get('user')

    if request.method == "POST":
        dict_ingredientes = {}   #Crea el diccionario para que puedas ser jsonificado
        for i in range(cantidad):
            ingrediente = request.form.get(f"producto{i}")
            cant = request.form.get(f"cantidad{i}")   #Ingresa los datos en el dict
            tipo = request.form.get(f"tipo{i}")
            valor = f"{cant} {tipo}"
            dict_ingredientes[ingrediente] = valor    #ACA HABRIA QUE JSONFICARLO Y QUE LO PUEDAN LLEVAR A LA API

        link_imagen = request.form.get("link_imagen")
        print(link_imagen)

        body = {
            'nombre': nombre,
            'ingredientes': dict_ingredientes,
            'duenio': duenio,
            'descripcion': descripcion,
            'imagen': link_imagen
        }

        # Realiza la solicitud a la API de backend
        api_url = f'http://127.0.0.1:5000/crear_receta'
        response = requests.post(api_url, json = body)

        return render_template("aceptado.html")

    return render_template('form_ingredientes.html',cantidad=cantidad, nombre=nombre, descripcion=descripcion)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run("127.0.0.1", port="8080", debug=True)
