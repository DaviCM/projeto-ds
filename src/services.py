from connection import get_connection
from time import sleep
from os import system

from passlib.hash import pbkdf2_sha256 as sha256

# Função que coleta o email do user e verifica se existe '@' - senão, não é um email.
def get_email(input_string): 
    while True:
        email = input(input_string)
        if '@' not in email:
            print('Email inválido. Por favor, insira outro.')
            sleep(1)
            system('cls')
            continue
        else:
            system('cls')
            return email
        
        
# Função que utiliza a lib passlib para gerar o hash sha256 para a senha
def get_password(input_string): 
    while True:
        pw_char = ''.join(input(input_string))
        pw = sha256.hash(pw_char)
        return pw
        
    
def create_table():
    try:
        con = get_connection()
        cursor = con.cursor() # Rodará os comandos, como o cursor do CMD
        
        cursor.execute(
            # Auto increment no sqlite3 é automático em primary key
            '''
            create table tb_usuario(
                
                id integer primary key, 
                nome varchar(120) not null,
                email varchar(120) unique,
                senha varchar(255)
            );     
            '''
        )
    
    except Exception as e:
        print(f'Não foi possível criar a tabela. Erro: {e}')
        
    finally:
        cursor.close()
        con.close()


def create_user(nome, email, senha):
    try:
        con = get_connection()
        cursor = con.cursor()
        
        nome = (input('Digite o nome do usuário a cadastrar: ').title()).strip()
        email = get_email('Digite o email a cadastrar: ')
        nome = get_password('Digite o nome do usuário a cadastrar: ')
        
        # Insert em SQL irá inserir um dado na tabela, nas colunas desejadas.
        cursor.execute('insert into tb_usuario(nome, email, senha) values(?, ?, ?);', 
                       (nome, email, senha)
        )
        
        con.commit()
        print(f'Usuário: {nome}')
        print(f'E-Mail: {email}')
        print(f'Senha: {senha} \n')
        print('Usuário cadastrado com sucesso!')
    
    except Exception as e:
        print(f'Não foi possível criar o usuário. Erro: {e}')
        
    finally:
        cursor.close()
        con.close()
    
    
def list_users():
    try:
        con = get_connection()
        cursor = con.cursor()
        cursor.execute('select nome, email, senha from tb_usuario')
        users = cursor.fetchall()
    
    except Exception as e:
        print(f'Não foi possível listar os usuários. Erro: {e}')
        
    finally:
        cursor.close()
        con.close()


def edit_user_info(id):
    try:
        con = get_connection()
        cursor = con.cursor()
    
    except Exception as e:
        print(f'Não foi possível acessar o usuário. Erro: {e}')
        
    finally:
        cursor.close()
        con.close()


def delete_user(id):
    try:
        con = get_connection()
        cursor = con.cursor()
    
    except Exception as e:
        print(f'Não foi possível excluir o usuário. Erro: {e}')
        
    finally:
        cursor.close()
        con.close()
    
     