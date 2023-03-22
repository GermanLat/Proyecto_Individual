from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.transaction import Transaction
from flask_app.models.user import User
from datetime import date

###TRANSACTIONS

#SEE TRANSACTIONS
#NEW EXPENSE
@app.route('/transaction/new')
def new_expense():
    validate_logged_in()
    data_D ={"date": date.today(),
            "transaction_as_id":session['user_id'],
            "bill_of_id":session['user_id']}
            #"transaction_category_id":1     #En la tabla de categorías (1: Gasto - Tipo Gasto; 2: Ingreso - Tipo Ingreso)
    return render_template('transaction_new.html', transaction_D=data_D, user=User.get_one_D({'id':session['user_id']}))

#USO??
#ADD TRANSACTION
@app.route('/transaction/add', methods=['POST'])
def add():
    if not Transaction.validate_B(request.form):
        print("error")
        return redirect("/transaction/new")
    Transaction.save_N(request.form)
    return redirect('/transaction/new')

#DELETE TRANSACTION
@app.route('/transaction/delete/<int:id>')
def destroy(id):
    data ={'id': id}
    Transaction.destroy(data)
    return redirect('/dashboard')

#UPDATE TRANSACTION
@app.route('/transaction/edit/<int:id>')
def edit(id):
    data_D = { "id" : id }
    return render_template('transaction_edit.html', transaction_D=data_D, user=User.get_one_D({'id':session['user_id']}), 
        transaction_to_edit=Transaction.get_one_C(data_D))

@app.route('/transaction/edit', methods=['POST'])
def update():
    if not Transaction.validate_B(request.form):
        return redirect("/transaction/edit/"+str(request.form['id']))
    Transaction.update(request.form)
    return redirect('/dashboard')

#FUNCIONES AUXILIARES PARA LOS CONTROLADORES
def validate_logged_in():   #Verifica si el usuario ingresó a la sesión, sino le redirige a la página de ingreso
    if session['logged_in'] != True:
        return redirect("/")