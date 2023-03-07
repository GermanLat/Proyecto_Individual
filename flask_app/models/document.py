from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import user
import inspect      #sirve para poder acceder al nombre de un método dentro del mismo, pudiendo servir para imprimirlo y detectar errores

class Document:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.pypie_id = data['pypie_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    #INSERT QUERIES
    @classmethod
    def save(cls, data):
        print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
        query = "INSERT INTO liked_pypies (user_id, pypie_id, created_at, updated_at) \
            VALUES (%(user_id)s, %(id)s, NOW(), NOW());"
        result = connectToMySQL('pypies_derby').query_db(query, data)
        print(result)
        print(f'Fin del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
        return result

    #SELECT QUERIES
    @classmethod
    def get_vote(cls, data):    #Revisa si en la tabla intermedia existe un voto del usuario al pie
        print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
        query = "SELECT * FROM liked_pypies\
            WHERE pypie_id = %(id)s AND user_id = %(user_id)s;"
        results = connectToMySQL('pypies_derby').query_db(query, data)
        if not results:    #Si la tabla está vacía, devuelve un diccionario vacío sino continúa
            return False
        print(f'Fin del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
        return True

    #DELETE QUERIES
    @classmethod
    def destroy(cls,data):
        print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
        query  = "DELETE FROM liked_pypies\
            WHERE pypie_id=%(id)s AND user_id=%(user_id)s;"
        print(f'Fin del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
        return connectToMySQL('pypies_derby').query_db(query,data)