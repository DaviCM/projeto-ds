from connection import get_connection
from time import sleep
from os import system

from passlib.hash import pbkdf2_sha256 as sha256

def proceed(message):
    system('cls')
    print(message)
    sleep(1)
    system('cls')


# Função que coleta o email do user e verifica se existe '@' - senão, não é um email.
def get_email(input_string): 
    while True:
        email = input(input_string)
        if '@' not in email:
            proceed('Email inválido. Por favor, insira outro.')
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


def get_int(message):
    while True:
        try:
            value = int(input(message).strip())
            return value
        except ValueError:
            proceed('Opção inválida. Tente novamente.')
            continue
            
    
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
        proceed(f'Não foi possível criar a tabela. Erro: {e}')
        
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
        proceed(f'Não foi possível criar o usuário. Erro: {e}')
        
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
        proceed(f'Não foi possível listar os usuários. Erro: {e}')
        
    finally:
        cursor.close()
        con.close()


def edit_user_info():
    while True:
        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute('select id, nome from tb_usuario')
            users = cursor.fetchall()

            opt = get_int('Insira o ID do usuário que deseja editar: ')

            if opt in users:
                print('\n''1 - Editar nome')
                print('2 - Editar e-mail')
                print('3 - Editar senha')
                
                opt = input('Insira a opção que deseja editar:').strip()
                match opt:
                    case '1':
                        nome = input('Insira o nome que deseja editar: ')
                        
                    case '2':
                        email = input('Insira o email que deseja editar:')
                        
                    case '3':
                        
                        
                    case '_':
                        
                
            else:
                proceed('O ID inserido não consta entre os usuários. Tente novamente.')
                continue 
    
        except Exception as e:
            proceed(f'Não foi possível acessar o usuário. Erro: {e}')
            break

        finally:
            cursor.close()
            con.close()
            break


def delete_user():
    try:
        con = get_connection()
        cursor = con.cursor()
        
        cursor.execute('delete from tb_usuario where id = ?', id)
    
    except Exception as e:
        proceed(f'Não foi possível excluir o usuário. Erro: {e}')
        
    finally:
        cursor.close()
        con.close()
    

