'''
import mysql
import mysql.connector

def get_connection():
    try:
        con =  mysql.connector.connect(
                host='195.179.238.1',
                user='u275872813_2ds',
                password='Controlegasto25',
                database='u275872813_controle_gasto'
            )
        
        if con.is_connected() == True:
            print('Deu bom')
            return con
        
    except Exception as e:
        print(f'Aconteceu um erro. Erro: {e}')
        return None


if __name__ == '__main__':        
    get_connection()
    
'''

import sqlite3

def get_connection():
    try:
        con = sqlite3.connect('controle_usuario.db')
        print('Conexão bem sucedida!')
        return con
        
    except Exception as e:
        print(f'Aconteceu um erro. Erro: {e}')
        return None


if __name__ == '__main__':        
    get_connection()
    
    