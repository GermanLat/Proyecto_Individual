from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from datetime import date, datetime
from flask_app.models import user
import inspect      #sirve para poder acceder al nombre de un método dentro del mismo, pudiendo servir para imprimirlo y detectar errores

schema_name="proyecto_individual"
table_name="transactions"

class Transaction:
    def __init__(self, data):
        self.id = data['id']
        self.date = data['date']
        self.amount = data['amount']
        self.description = data['description']
        self.document_id = data['document_id']
        self.transaction_as_id = data['transaction_as_id']
        self.bill_of_id = data['bill_of_id']
        self.transaction_category_id = data['transaction_category_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.lista=[]   #aún no sé lista de qué será

    #VALIDACIONES
    @classmethod    #Debería ser @staticmethod porque no necesito pasarle cls o self pero uso @classmethod para poder rastrear el paso 
                    #   por este Método
    def validate_B(cls, user_D):
        print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
        is_valid = True # asumimos que esto es true
        print(f'Fin del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
        return is_valid
    
    #INSERT QUERIES
    @classmethod
    def save_N(cls, data_D):
        print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
        query = "INSERT INTO " + table_name + " (date, amount, description, transaction_as_id, \
            bill_of_id, transaction_category_id, created_at, updated_at) \
            VALUES (%(date)s, %(amount)s, %(description)s, %(transaction_as_id)s, \
            %(bill_of_id)s, %(transaction_category_id)s, NOW(), NOW());" #document_id = %(document_id)s falta incorporar
        result_N = connectToMySQL(schema_name).query_db(query, data_D)
        print(f'Fin del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
        return result_N

    #SELECT QUERIES
    @classmethod    #usar @classmethod siempre que consulte a la base de datos
    def get_all_LD(cls):
        query = "SELECT * FROM transactions;"
        results_LD = connectToMySQL(schema_name).query_db(query)
        if len(results_LD)==0:
            results_LD=[{'id':"", 'date':"", 'amount':"", 'description':"", 'document_id':"", 'transaction_as_id':"", 'bill_of_id':"", 
                'transaction_category_id':"", 'created_at':"", 'updated_at':""}]
        return results_LD
    
    @classmethod
    def get_one(cls,data):
        print(f'Inicio del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
        query  = "SELECT * FROM transactions WHERE id = %(id)s;"
        result = connectToMySQL(schema_name).query_db(query,data)
        print(f'Fin del módulo {inspect.stack()[0][3]}() \t- \tClass: {cls.__name__}')
        return cls(result[0])
    
    #SELECT QUERIES
    @classmethod    #usar @classmethod siempre que consulte a la base de datos
    def get_total_LD(cls):
        query = "SELECT SUM(amount) as 'total' FROM transactions WHERE id>0;"
        results_LD = connectToMySQL(schema_name).query_db(query)
        if len(results_LD)==0:
            results_LD=[{'total':0}]
        print(results_LD[0]['total'])
        print("get_total_LD TRANSACTION\n")
        return results_LD[0]['total']
    
    #SELECT QUERIES
    @classmethod    #usar @classmethod siempre que consulte a la base de datos
    def get_total_by_user_LD(cls, data_D):
        query = "SELECT user_id, SUM(monto) as 'total' FROM transactions WHERE user_id=%(id)s;"
        results_LD = connectToMySQL(schema_name).query_db(query, data_D)
        if len(results_LD)==0:
            results_LD=[{'total':0}]
        print(results_LD)
        print("get_total_by_user_LD TRANSACTION\n")
        return results_LD[0]['total']

    @classmethod
    def get_one_C(cls, data_D):
        query  = "SELECT * FROM transactions WHERE id = %(id)s;"
        results_LD = connectToMySQL(schema_name).query_db(query, data_D)
        return cls(results_LD[0])

    #UPDATE QUERIES
    @classmethod
    def update(cls, data_D):
        query = "UPDATE transactions SET date=%(date)s, amount=%(amount)s, description=%(description)s, document_id=%(document_id)s, \
            transaction_as_id=%(transaction_as_id)s, bill_of_id=%(bill_of_id)s, transaction_category_id=%(transaction_category_id)s, \
            updated_at=NOW() WHERE id = %(id)s;"
        print("update TRANSACTION\n")
        return connectToMySQL(schema_name).query_db(query, data_D)

    #DELETE QUERIES
    @classmethod
    def destroy(cls, data_D):
        query  = "DELETE FROM transactions WHERE id = %(id)s;"
        print("destroy TRANSACTION\n")
        return connectToMySQL(schema_name).query_db(query, data_D)