from flask import Flask, request, render_template, redirect, url_for, send_from_directory, session
import requests
import os


app = Flask(__name__)
app.secret_key = os.urandom(15)       # La secret_key es necesaria para validar sesiones de usuarios


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
    platos_json_api = response.json()       # Nombre y descripcion de los platos de la database
    
    return render_template('menu.html', platosjson=platos_json_api)

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        username_form = request.form.get('username_form')
        password_form = request.form.get('password_form')
            
        # Realiza la solicitud a la API de backend
        api_url = f'http://127.0.0.1:5000/login/{username_form}'
        response = requests.get(api_url)
        assigned_password = response.json()       # Contraseña asignada al usuario en la database

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

        body = {
            'nombre': nombre,
            'ingredientes': dict_ingredientes,
            'duenio': duenio,
            'descripcion': descripcion
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