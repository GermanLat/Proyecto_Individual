from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re   # el módulo regex
from datetime import date, datetime
from flask_app.models import natural_person, legal_person, transaction, document
import inspect      #sirve para poder acceder al nombre de un método dentro del mismo, pudiendo servir para imprimirlo y detectar errores

# crea un objeto de expresión regular que usaremos más adelante
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

schema_name="proyecto_individual"
table_name="users"

class User:
    def __init__(self, data):
        self.id = data['id']
        self.natural_person_id = data['natural_person_id']
        self.legal_person_id = data['legal_person_id']
        self.email = data['email']
        self.ruc = data['ruc']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.transactions=[]

    ###USANDOSE
    #VALIDACIONES
    @classmethod    #Debería ser @staticmethod porque no necesito pasarle cls o self pero uso @classmethod para poder rastrear el paso 
                    #   por este Método
    def validate_B(cls, user_D):
        print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
        is_valid = True # asumimos que esto es true
        if not EMAIL_REGEX.match(user_D['email'])  or user_D['email'] == "": 
            flash("Invalid email address.", "register")
            is_valid = False
        elif User.get_by_email_C(user_D):
            flash("Email address already register.", "register")
            is_valid = False
        if len(user_D['ruc']) < 6 or not user_D['ruc'][0:-3].isalnum() or not user_D['ruc'][-2]=="-" or not user_D['ruc'][-1].isalnum():
            flash("RUC must have at least 6 characters and all alphanumeric characters except one '-' at the second last position.", "register")
            is_valid = False
        if len(user_D['password']) < 8:
            flash("Password must be at least 8 characters.", "register")
            is_valid = False
        if user_D['password'] != user_D['confirm_password']:
            flash("Password confirmation failed.", "register")
            is_valid = False
        print(f'Fin del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
        return is_valid
    
    ###USANDOSE
    #INSERT QUERIES
    @classmethod
    def save_N(cls, data_D):
        print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
        query = "INSERT INTO " + table_name + " (natural_person_id, legal_person_id, email, ruc, password, created_at, updated_at) \
            VALUES (%(natural_person_id)s, %(legal_person_id)s, %(email)s, %(ruc)s, %(password)s, NOW(), NOW());"
        result = connectToMySQL(schema_name).query_db(query, data_D)
        print(f'Fin del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
        return result
    
    # #SELECT QUERIES
    # @classmethod    #usar @classmethod siempre que consulte a la base de datos
    # def get_all_LC(cls):
    #     print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
    #     query = "SELECT * FROM " + table_name + ";"
    #     results = connectToMySQL(schema_name).query_db(query)
    #     instances_list = []
    #     for r in results:
    #         instances_list.append( cls(r) )
    #     print(f'Fin del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
    #     return instances_list
    
    ###USANDOSE
    #SELECT QUERIES (ONE TO ONE)
    @classmethod
    def get_one_C(cls, data_D):
        print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
        query  = "SELECT * FROM " + table_name + "\
                LEFT JOIN natural_persons ON users.natural_person_id=natural_persons.id\
                LEFT JOIN legal_persons ON users.legal_person_id=legal_persons.id\
                WHERE users.id = %(id)s;"
        result = connectToMySQL(schema_name).query_db(query, data_D)
        print(result)
        if result[0]["natural_person_id"]:
            query  = "SELECT users.id as id, natural_persons.identity_document as identity_document,\
                CONCAT(natural_persons.first_name, ' ', natural_persons.last_name) as complete_name, users.email as email,\
                users.ruc as ruc, users.password as password FROM " + table_name + "\
                LEFT JOIN natural_persons ON users.natural_person_id=natural_persons.id\
                WHERE users.id = %(id)s;"
        if result[0]["legal_person_id"]:
            query  = "SELECT users.id as id, null as identity_document,\
                legal_persons.name as complete_name, users.email as email,\
                users.ruc as ruc, users.password as password FROM " + table_name + "\
                LEFT JOIN legal_persons ON users.legal_person_id=legal_persons.id\
                WHERE users.id = %(id)s;"
        result = connectToMySQL(schema_name).query_db(query, data_D)
        if len(result)<1:       #AQUI ESTARIA MAL SI NO ENCUENTRA NADA PORQUE DEVOLVERIA UNA LISTA EN VEZ DE UNA CLASE
            return {}
        print(f'Fin del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
        return cls(result[0])
    
    ###USANDOSE
    @classmethod
    def get_by_email_C(cls, data_D): #devuelve el Id del usuario al que pertenece el email, sino existe devuelve falso
        print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
        query = "SELECT * FROM " + table_name + " WHERE email = %(email)s;"
        result = connectToMySQL(schema_name).query_db(query, data_D)
        # no se encontró un usuario coincidente
        if len(result) < 1:
            return {}
        print(result[0])
        print(f'Fin del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
        return cls(result[0])   #Retorno una instancia de la clase, por eso me refiero con .id al id del usuario ???????????
    
    # #UPDATE QUERIES
    # @classmethod
    # def update(cls, data):
    #     print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
    #     query = "UPDATE " + table_name + " SET natural_person_id=%(natural_person_id)s, \
    #         legal_person_id=%(legal_person_id)s, email=%(email)s, ruc=%(ruc)s, \
    #         password=%(password)s, updated_at=NOW() WHERE id = %(id)s;"
    #     print(f'Fin del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
    #     return connectToMySQL(schema_name).query_db(query, data)
    
    # #DELETE QUERIES
    # @classmethod
    # def destroy(cls, data):
    #     print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
    #     query  = "DELETE FROM " + table_name + " WHERE id = %(id)s;"
    #     print(f'Fin del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
    #     return connectToMySQL(schema_name).query_db(query, data)




    # #SELECT QUERIES (ONE TO MANY)
    # @classmethod
    # def pypies_by_one(cls, data):
    #     print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
    #     query = "SELECT * FROM users \
    #         LEFT JOIN pypies ON users.id=pypies.autor_id \
    #         WHERE users.id = %(id)s;"
    #     results = connectToMySQL(schema_name).query_db(query, data)
    #     if len(results) < 1:        #Si la tabla está vacía, devuelve un diccionario vacío sino continúa
    #         return {}
    #     # creamos una instancia de la clase, para que se cree el self._____=[] y poder almacenar los diccionarios de resultados
    #     pypies_by_one = cls( results[0] )     #Si hubiesemos buscado el primer elemento de una lista vacía, nos iba a dar error
    #     for row_from_db in results:     # crearemos una lista de instancias de pypies para el id
    #         pypies_data = {
    #             "id" : row_from_db["pypies.id"],
    #             "name" : row_from_db["name"],
    #             "filling" : row_from_db["filling"],
    #             "crust" : row_from_db["crust"],
    #             "autor_id" : row_from_db["autor_id"],
    #             "created_at" : row_from_db["pypies.created_at"],
    #             "updated_at" : row_from_db["pypies.updated_at"]
    #         }
    #         pypies_by_one.pypies.append( pypie.Pypie(pypies_data) )
    #     print(f'Fin del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
    #     return pypies_by_one