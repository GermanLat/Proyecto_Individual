from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from datetime import date, datetime
from flask_app.models import user
import inspect      #sirve para poder acceder al nombre de un método dentro del mismo, pudiendo servir para imprimirlo y detectar errores

class Transaction:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.filling = data['filling']
        self.crust = data['crust']
        self.autor_id = data['autor_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users=[]

    #VALIDACIONES
    @classmethod    #Debería ser @staticmethod porque no necesito pasarle cls o self pero uso @classmethod para poder rastrear el paso 
                    #   por este Método
    def validate_pypie(cls, pypie):
        print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
        is_valid = True # asumimos que esto es true
        if len(pypie['name']) < 3:
            flash("Name must have at least 3 characters.", "new_pypie")
            is_valid = False
        if len(pypie['filling']) < 3:
            flash("Filling must have at least 3 characters.", "new_pypie")
            is_valid = False
        if len(pypie['crust']) < 3:
            flash("Crust must have at least 3 characters.", "new_pypie")
            is_valid = False
        print(f'Fin del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
        return is_valid
    
    #INSERT QUERIES
    @classmethod
    def save(cls, data):
        print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
        query = "INSERT INTO pypies (name, filling, crust, autor_id, created_at, updated_at) \
            VALUES (%(name)s, %(filling)s, %(crust)s, %(autor_id)s, NOW(), NOW());"
        result = connectToMySQL('pypies_derby').query_db(query, data)
        print(f'Fin del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
        return result

    #SELECT QUERIES
    @classmethod    #usar @classmethod siempre que consulte a la base de datos
    def get_all(cls):
        print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
        query = "SELECT * FROM pypies;"
        results = connectToMySQL('pypies_derby').query_db(query)
        pypies = []
        for r in results:
            pypies.append( cls(r) )
        print(f'Fin del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
        return pypies
    
    @classmethod
    def get_one(cls,data):
        print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
        query  = "SELECT * FROM pypies WHERE id = %(id)s;"
        result = connectToMySQL('pypies_derby').query_db(query,data)
        print(f'Fin del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
        return cls(result[0])

    @classmethod
    def get_by_autor_id(cls,data): #devuelve el Id del usuario al que pertenece el email, sino existe devuelve falso
        print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
        query = "SELECT * FROM pypies WHERE autor_id = %(autor_id)s;"
        result = connectToMySQL("pypies_derby").query_db(query,data)
        # no se encontró un usuario coincidente
        if len(result) < 1:
            return False
        print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
        return cls(result[0])   #Retorno una instancia de la clase, por eso me refiero con .id al id del usuario
    
    #SELECT QUERIES (ONE TO ONE)
    @classmethod
    def get_one_with_autor(cls, data):
        print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
        query = "SELECT * FROM pypies \
            LEFT JOIN users ON users.id=pypies.autor_id \
            WHERE pypies.id = %(id)s;"
        result = connectToMySQL('pypies_derby').query_db(query, data)
        if len(result) < 1:        #Si la tabla está vacía, devuelve un diccionario vacío sino continúa
            return {}
        get_one_with_autor=result[0]
        # creamos una instancia de la clase, para que se cree el self._____=[] y poder almacenar los diccionarios de resultados
        pypies_data = {
            "id" : get_one_with_autor["id"],
            "name" : get_one_with_autor["name"],
            "filling" : get_one_with_autor["filling"],
            "crust" : get_one_with_autor["crust"],
            "autor_id" : get_one_with_autor["autor_id"],
            "autor" : get_one_with_autor["first_name"]+' '+get_one_with_autor["last_name"],
            "created_at" : get_one_with_autor["created_at"],
            "updated_at" : get_one_with_autor["updated_at"]
        }
        print(f'Fin del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
        return pypies_data

    #SELECT QUERIES (MANY TO MANY)
    @classmethod
    def group_by_votes(cls):
        print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
        query = "SELECT pypies.id, pypies.name, CONCAT(autors.first_name,' ',autors.last_name) as 'PyPie By', pypies.filling, pypies.crust, COUNT(liked_pypies.pypie_id) as Votes FROM pypies\
            LEFT JOIN liked_pypies ON pypies.id=liked_pypies.pypie_id\
            LEFT JOIN users ON users.id=liked_pypies.user_id\
            LEFT JOIN users as autors ON autors.id=pypies.autor_id\
            GROUP BY pypies.id\
            ORDER BY COUNT(liked_pypies.pypie_id) DESC;"
        results = connectToMySQL('pypies_derby').query_db(query)
        print(results)
        if len(results) < 1:    #Si la tabla está vacía, devuelve un diccionario vacío sino continúa
            return {}
        print(f'Fin del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
        return results
    
    #UPDATE QUERIES
    @classmethod
    def update(cls,data):
        print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
        query = "UPDATE pypies SET name=%(name)s,filling=%(filling)s,crust=%(crust)s,updated_at=NOW() WHERE id = %(id)s;"
        print(f'Fin del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
        return connectToMySQL('pypies_derby').query_db(query,data)

    #DELETE QUERIES
    @classmethod
    def destroy(cls,data):
        print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
        query  = "DELETE FROM pypies WHERE id = %(id)s;"
        print(f'Fin del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
        return connectToMySQL('pypies_derby').query_db(query,data)