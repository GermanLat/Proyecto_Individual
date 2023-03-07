from flask import render_template, request, redirect, session
from flask_app import app
from flask_app.controllers import users, transactions, documents

if __name__=="__main__":
    app.run(debug=True)

#The function the letter of what return, the variable of what requiere
#B: Boolean
#C: Class instance
#D: Dictionary
#L: List
#N: Number
#S: String