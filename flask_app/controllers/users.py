from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models.user import User
from flask_app.models.natural_person import Natural_Person
from flask_app.models.legal_person import Legal_Person
from flask_app.models.transaction import Transaction
from flask_app.models.document import Document
import inspect      #sirve para poder acceder al nombre de un método dentro del mismo, pudiendo servir para imprimirlo y detectar errores

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)    # estamos creando un objeto llamado bcrypt,
                        # que se realiza invocando la función Bcrypt con nuestra aplicación como argumento
from flask import flash

###USANDOSE
#PÁGINA DE LOGIN
@app.route('/')
def login_page():
    print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tPath: {request.path} \t- \tMétodo: {request.method}')
    print(f'Fin del módulo {inspect.stack()[0][3]}() \t- \tPath: {request.path} \t- \tMétodo: {request.method}')
    return render_template("index.html")

###USANDOSE
#PÁGINA DE REGISTRO
@app.route('/register')
def register_page():
    print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tPath: {request.path} \t- \tMétodo: {request.method}')
    print(f'Fin del módulo {inspect.stack()[0][3]}() \t- \tPath: {request.path} \t- \tMétodo: {request.method}')
    return render_template("register.html")

###USANDOSE
#INGRESO A LA PLATAFORMA
@app.route('/register/process', methods=['POST'])
def process_register():
    print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tPath: {request.path} \t- \tMétodo: {request.method}')
    user_type=request.form['user_type']
    is_valid = True
    if not User.validate_B(request.form):
        is_valid = False
    if request.form['user_type']=="natural_person":
        if not Natural_Person.validate_B(request.form):
            is_valid = False
        if is_valid==False:
            return redirect("/register")
        data_user_type = {
            "identity_document": request.form['identity_document'],
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name']
        }
        user_type_id = Natural_Person.save_N(data_user_type)
        data_user = {
            "natural_person_id": user_type_id,
            "legal_person_id": None
        }
    elif request.form['user_type']=="legal_person":
        if not Legal_Person.validate_B(request.form):
            is_valid = False
        if is_valid==False:
            return redirect("/register")
        data_user_type = {
            "name": request.form['name'],
            "business_name": request.form['business_name']
        }
        user_type_id = Legal_Person.save_N(data_user_type)
        data_user = {
            "natural_person_id": None,
            "legal_person_id": user_type_id
        }
    else:
        return redirect("/register")
    if is_valid==False:
        return redirect("/register")
    # crear el hash
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    # poner pw_hash en el diccionario de datos
    data_user["email"] = request.form['email']
    data_user["ruc"] = request.form['ruc']
    data_user["password"] = pw_hash
    # llama al @classmethod de guardado en Usuario
    user_id = User.save_N(data_user)
    # almacenar id de usuario en la sesión
    session['user_id'] = user_id
    session['logged_in'] = True
    print(f'Fin del módulo {inspect.stack()[0][3]}() \t- \tPath: {request.path} \t- \tMétodo: {request.method}')
    return redirect("/dashboard")

###USANDOSE
#POST: LOGIN PAGE
@app.route('/login', methods=['POST'])
def login():
    print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tPath: {request.path} \t- \tMétodo: {request.method}')
    # ver si el nombre de usuario proporcionado existe en la base de datos
    data_D = { "email" : request.form["email"] }
    user_C = User.get_by_email_C(data_D)
    # usuario no está registrado en la base de datos
    if not user_C:
        flash("Invalid Email/Password", "login")
        return redirect("/")
    # módulo de la librería bcrypt que verifica si la contraseña es correcta
    if not bcrypt.check_password_hash(user_C.password, request.form['password']):
        # si obtenemos False después de verificar la contraseña
        flash("Invalid Email/Password", "login")
        return redirect('/')
    # si las contraseñas coinciden, configuramos el user_id en sesión
    session['user_id'] = user_C.id
    session['logged_in'] = True
    print(f'Fin del módulo {inspect.stack()[0][3]}() \t- \tPath: {request.path} \t- \tMétodo: {request.method}')
    return redirect("/dashboard")

###USANDOSE - NECESITA QUE SE LE PASEN LOS DATOS DE LAS TRANSACCIONES
#DASHBOARD PAGE
@app.route('/dashboard')
def dashboard():
    print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tPath: {request.path} \t- \tMétodo: {request.method}')
    validate_logged_in()
    data_D ={"id":session['user_id']}     #Id del usuario guardado en "Session"
    print(f'Fin del módulo {inspect.stack()[0][3]}() \t- \tPath: {request.path} \t- \tMétodo: {request.method}')
    return render_template("dashboard.html", user_C=User.get_one_C(data_D))

# #ADD PIE
# @app.route('/add', methods=['POST'])
# def add():
#     print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tPath: {request.path} \t- \tMétodo: {request.method}')
#     if not Pypie.validate_pypie(request.form):
#         return redirect("/dashboard")
#     Pypie.save(request.form)
#     print(f'Fin del módulo {inspect.stack()[0][3]}() \t- \tPath: {request.path} \t- \tMétodo: {request.method}')
#     return redirect('/dashboard')

# #EDIT PIE
# @app.route('/edit/<int:id>')
# def edit(id):
#     print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tPath: {request.path} \t- \tMétodo: {request.method}')
#     data = { "id" : id }
#     print(f'Fin del módulo {inspect.stack()[0][3]}() \t- \tPath: {request.path} \t- \tMétodo: {request.method}')
#     return render_template('edit_pie.html', pypie=Pypie.get_one(data))

# @app.route('/edit',methods=['POST'])
# def update():
#     print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tPath: {request.path} \t- \tMétodo: {request.method}')
#     print(request.form['id'])
#     if not Pypie.validate_pypie(request.form):
#         return redirect("/edit/"+str(request.form['id']))
#     Pypie.update(request.form)
#     print(f'Fin del módulo {inspect.stack()[0][3]}() \t- \tPath: {request.path} \t- \tMétodo: {request.method}')
#     return redirect('/dashboard')

# #DELETE PIE
# @app.route('/delete/<int:id>')
# def destroy(id):
#     print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tPath: {request.path} \t- \tMétodo: {request.method}')
#     data ={'id': id}
#     Pypie.destroy(data)
#     print(f'Fin del módulo {inspect.stack()[0][3]}() \t- \tPath: {request.path} \t- \tMétodo: {request.method}')
#     return redirect('/dashboard')

# #RANKING
# @app.route('/pies')
# def derby():
#     print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tPath: {request.path} \t- \tMétodo: {request.method}')
#     print(f'Fin del módulo {inspect.stack()[0][3]}() \t- \tPath: {request.path} \t- \tMétodo: {request.method}')
#     return render_template('all_pies.html', all_pypies=Pypie.group_by_votes())

# #SHOW PIE
# @app.route('/show/<int:id>')
# def show(id):
#     print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tPath: {request.path} \t- \tMétodo: {request.method}')
#     data ={'id': id}
#     print(f'Fin del módulo {inspect.stack()[0][3]}() \t- \tPath: {request.path} \t- \tMétodo: {request.method}')
#     return render_template('show_pie.html', pypie=Pypie.get_one_with_autor(data))

# #VOTE PIE
# @app.route('/vote/<int:id>')    #Revisa si hay voto, si hay lo borra, sino lo agrega
# def vote(id):
#     print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tPath: {request.path} \t- \tMétodo: {request.method}')
#     data ={
#         'id': id,
#         'user_id': session['user_id']
#     }
#     if Liked_pypie.get_vote(data):
#         Liked_pypie.destroy(data)
#     else:
#         Liked_pypie.save(data)
#     print(f'Fin del módulo {inspect.stack()[0][3]}() \t- \tPath: {request.path} \t- \tMétodo: {request.method}')
#     return render_template('show_pie.html', pypie=Pypie.get_one_with_autor(data))

###USANDOSE
#LOGOUT
@app.route('/logout')
def logout():
    print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tPath: {request.path} \t- \tMétodo: {request.method}')
    session['user_id'] =''
    session['logged_in'] =False
    print(f'Fin del módulo {inspect.stack()[0][3]}() \t- \tPath: {request.path} \t- \tMétodo: {request.method}')
    return redirect("/")

#FUNCIONES AUXILIARES PARA LOS CONTROLADORES

#Podría estar dentro de los Modelos siendo que no se ejecuta a través de una ruta nueva pero redirige a un ruta por eso pienso que 
#   es mejor dentro de los Controladores
#A través de una ruta nueva no podría hacer que se ejecute porque esto se realiza al inicio de cada ruta
#Puedo colocar el código dentro de varias rutas existentes con el método GET (si escribís en el navegador una url del método POST,
#   siempre da página de error) pero sería repetir 2 líneas muchas veces, en lugar de 1 línea
def validate_logged_in():   #Verifica si el usuario ingresó a la sesión, sino le redirige a la página de ingreso
    print(f'Inicio del módulo {inspect.stack()[0][3]}()')
    if session['logged_in'] != True:
        return redirect("/")
    print(f'Fin del módulo {inspect.stack()[0][3]}()')






# @app.route('/paintings/new')
# def new_painting():
#     print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tPath: {request.path} \t- \tMétodo: {request.method}')
#     validate_logged_in()
#     print(f'Fin del módulo {inspect.stack()[0][3]}() \t- \tPath: {request.path} \t- \tMétodo: {request.method}')
#     return render_template("new_painting.html")

# @app.route('/paintings/add', methods=['POST'])            #ACA ME QUEDE!!!!!!!
# def add_painting():
#     print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tPath: {request.path} \t- \tMétodo: {request.method}')
#     if not Painting.validate_painting(request.form):
#         return redirect("/")
#     data = {
#         "autor_id": session["user_id"],
#         "title": request.form['title'],
#         "description": request.form['description'],
#         "price": request.form['price'],
#         "quantity_created": request.form['quantity_created'],
#         "quantity_buyed": 0,
#         "posted": True
#     }
#     print(Painting.save(data))
#     print(f'Fin del módulo {inspect.stack()[0][3]}() \t- \tPath: {request.path} \t- \tMétodo: {request.method}')
#     return redirect("/paintings")


