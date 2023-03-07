from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import transaction, document
import inspect      #sirve para poder acceder al nombre de un método dentro del mismo, pudiendo servir para imprimirlo y detectar errores

schema_name="proyecto_individual"
table_name="legal_persons"

class Legal_Person:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.business_name = data['business_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.transactions=[]

    ###USANDOSE
    #VALIDATIONS
    @classmethod    #Debería ser @staticmethod porque no necesito pasarle cls o self pero uso @classmethod para poder rastrear el paso 
                    #   por este Método
    def validate_B(cls, user_D):
        print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
        is_valid = True # asumimos que esto es true
        if len(user_D['name']) < 2:
            flash("Name must have at least 2 characters.", "register")
            is_valid = False
        if len(user_D['business_name']) < 2:
            flash("Business name must have at least 2 characters.", "register")
            is_valid = False
        print(f'Fin del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
        return is_valid
    
    ###USANDOSE
    #INSERT QUERIES
    @classmethod
    def save_N(cls, data_D):
        print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
        query = "INSERT INTO " + table_name + " (name, business_name, created_at, updated_at) \
            VALUES (%(name)s, %(business_name)s, NOW(), NOW());"
        result = connectToMySQL(schema_name).query_db(query, data_D)
        print(f'Fin del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
        return result
    
    # #SELECT QUERIES
    # @classmethod
    # def get_all_LC(cls):
    #     print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
    #     query = "SELECT * FROM " + table_name + ";"
    #     results = connectToMySQL(schema_name).query_db(query)
    #     instances_list = []
    #     for r in results:
    #         instances_list.append( cls(r) )
    #     print(f'Fin del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
    #     return instances_list
    
    # @classmethod
    # def get_one_C(cls, data):
    #     print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
    #     query  = "SELECT * FROM " + table_name + "WHERE id = %(id)s;"
    #     result = connectToMySQL(schema_name).query_db(query,data)
    #     print(f'Fin del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
    #     return cls(result[0])
    
    # #UPDATE QUERIES
    # @classmethod
    # def update(cls,data):
    #     print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
    #     query = "UPDATE " + table_name + " SET name=%(name)s, \
    #         business_name=%(business_name)s, updated_at=NOW() WHERE id = %(id)s;"
    #     print(f'Fin del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
    #     return connectToMySQL(schema_name).query_db(query,data)
    
    # #DELETE QUERIES
    # @classmethod
    # def destroy(cls,data):
    #     print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
    #     query  = "DELETE FROM " + table_name + " WHERE id = %(id)s;"
    #     print(f'Fin del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
    #     return connectToMySQL(schema_name).query_db(query,data)



    # @classmethod
    # def get_by_email_C(cls, data): #devuelve el Id del usuario al que pertenece el email, sino existe devuelve falso
    #     print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
    #     query = "SELECT * FROM " + table_name + "WHERE email = %(email)s;"
    #     result = connectToMySQL(schema_name).query_db(query,data)
    #     # no se encontró un usuario coincidente
    #     if len(result) < 1:
    #         return {}
    #     print(f'Fin del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
    #     return cls(result[0])   #Retorno una instancia de la clase, por eso me refiero con .id al id del usuario

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