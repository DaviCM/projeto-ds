import sqlite3

def get_connection():
    try:
        con = sqlite3.connect('./db/controle_usuario.db')
        return con, con.cursor()
        
    except Exception as e:
        print(f'Aconteceu um erro. Erro: {e}')
        return None, None


if __name__ == '__main__':        
    get_connection()
    
    