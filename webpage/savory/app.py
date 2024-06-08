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
            session['auth'] = True                  # Autentica la sesion del usuario
            session['user'] = username_form          # Asigna el username autenticado en la sesion
            return redirect(url_for('suggest',username=username_form))


    return render_template('login.html')

@app.route('/suggest/<username>')
def suggest(username):
    if not session.get('auth'):           # Si la sesion no esta autenticada, lo devuelve al login
        return redirect(url_for('login'))
    
    if session.get('user') != username:         # Si el username no es igual al autenticado en la sesion, lo devuelve al login
        return redirect(url_for('login'))

    return f'Acceso exitoso. Bienvenido {username}'

    # En esta funcion se va a usar el endpoint POST de la api


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run("127.0.0.1", port="8080", debug=True)