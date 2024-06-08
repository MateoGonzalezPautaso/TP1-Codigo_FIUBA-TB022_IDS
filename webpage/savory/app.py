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
    return render_template('menu.html')

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
            session['auth'] = True             # Autentica la sesion del usuario
            return redirect(url_for('suggest',username=username_form))


    return render_template('login.html')

@app.route('/suggest/<username>', methods=["GET","POST"])
def suggest(username):
    if not session.get('auth'):           # Si la sesion no esta autenticada, lo devuelve al login
        return redirect(url_for('login'))
    if request.method == "POST":         #Si es metodo post(ya se completo el primer form), guarda la cantidad de campos a usar
        cantidad = int(request.form.get("numIngredientes"))
        nombre = int(request.form.get("namePlato"))      #Estos 2 datos tienen que ser enviados a la api pra meterlos en la BBDD
        descripcion = int(request.form.get("descPlato"))
        return redirect(url_for('suggest_ingredientes', cantidad=cantidad, _external=True))    #Redirecciona a el forms de ingredientes, pasando la cantidad de campos
        
    return render_template("form_receta.html")

    # En esta funcion se va a usar el endpoint POST de la api


@app.route('/suggest/ingredientes/', methods=["GET","POST"])
def suggest_ingredientes():
    cantidad = int(request.args.get('cantidad'))   #Recibe cantidad como argumento
    if request.method == "POST":
        dict_ingredientes = {}   #Crea el diccionario para que puedas ser jsonificado
        for i in range(cantidad):
            ingrediente = request.form.get(f"producto{i}")
            cant = request.form.get(f"cantidad{i}")   #Ingresa los datos en el dict
            dict_ingredientes[ingrediente] = cant    #ACA HABRIA QUE JSONFICARLO Y QUE LO PUEDAN LLEVAR A LA API
        return render_template("aceptado.html")
    return render_template('form_ingredientes.html', cantidad=cantidad)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run("127.0.0.1", port="8080", debug=True)