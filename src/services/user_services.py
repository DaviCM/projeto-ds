from connection import get_connection
from services.proceed import *
from getpass import getpass
from passlib.hash import pbkdf2_sha256 as sha256

class GetEmailModeError(Exception):
    def __init__(self, msg='Passou parâmetro inexistente para modo. Opções são (signup) e (query).'):
        self.msg = msg
        super.__init__(self.msg)
        
        

# Função que coleta o email do user e verifica se existe '@' - senão, não é um email.
def get_email(input_str, mode='query'):
    while True:
        con, cursor = get_connection()
        cursor.execute('select email from tb_usuario')
        executed = cursor.fetchall()
        
        # lista de tuplas, tenho que tratar
        emails = [e[0] for e in executed] # itera sobre cada tupla '(email@a,)' e pega seu elemento 0, no caso 'email@a'
        email = input(input_str).strip()
        
        try:
            if (
                (mode == 'signup') and (('@' not in email) or (email in emails)) 
                or (mode == 'query') and ('@' not in email)
                ):
                proceed('E-mail inválido. Tente novamente.')
                continue
            elif (mode == 'signup' or 'query'):
                return email
            else:
                raise GetEmailModeError
        except Exception as e:
            proceed(f'Não foi possível acessar a lista de e-mails. Retornando ao menu principal. Erro: {e}')
            return None
        finally:
            cursor.close()
            con.close()
        
        
# Função que utiliza a lib passlib para gerar o hash sha256 da a senha
def get_password(string, hashed=True): 
    while True:
        pw_char = ''.join(string)
        pw = sha256.hash(pw_char)
        return pw if hashed == True else pw_char


def get_int(message):
    while True:
        try:
            value = int(input(message).strip())
            return value
        except ValueError:
            proceed('Opção inválida. Tente novamente.')
            continue
            

def log_in(get_user=False):
    while True:
        try:
            con, cursor = get_connection()

            email = get_email('Insira seu email: ')
            senha = get_password(getpass('Insira sua senha: '), hashed=False)

            cursor.execute('select id, senha from tb_usuario where email = ?', (email,)) 
            result = cursor.fetchone()
            
            if None in result:
                proceed('E-mail ou senha não encontrados. Tente novamente.')
                continue

            id, found_pw = result
            
            if sha256.verify(senha, found_pw) == False:
                proceed('E-mail encontrado e senha incorreta. Tente novamente.')
                continue
            elif get_user == True:
                cursor.execute('select nome from tb_usuario where email = ?', (email,))
                nome = cursor.fetchone()[0]
                return nome, email
            else:
                check = True
                return check, id
        except TypeError:
            proceed('Não foi possível encontrar o usuário. Reiniciando.')
            continue
        except Exception as e:
            proceed(f'Ocorreu um problema com o sistema. Erro: {e}')
            break
        finally:
            cursor.close()
            con.close()

 
def create_table():
    try:
        con, cursor = get_connection() # Cursor Rodará os comandos, como o cursor do CMD
        cursor.execute(
            # Auto increment no sqlite3 é automático em primary key
            '''
            create table if not exists tb_usuario(
                
                id integer primary key, 
                nome varchar(120) not null,
                email varchar(120) unique,
                senha varchar(255)
            );     
            '''
        )
        proceed('Tabela criada com sucesso!')
    except Exception as e:
        proceed(f'Não foi possível criar a tabela. Erro: {e}')
    finally:
        cursor.close()
        con.close()


def create_user():
    while True:
        try:
            con, cursor = get_connection()
            
            nome = (input('Digite seu nome: ').title()).strip()
            email = get_email('Digite seu e-mail: ', mode='signup')
            senha = get_password(getpass('Digite sua senha: '))
            
            # Insert em SQL irá inserir um dado na tabela, nas colunas desejadas.
            cursor.execute('insert into tb_usuario(nome, email, senha) values(?, ?, ?);', 
                           (nome, email, senha)
            )
            
            con.commit()
            proceed('Usuário cadastrado com sucesso!')
            print(f'Usuário: {nome}')
            print(f'E-Mail: {email}')
            proceed('Retornando ao menu principal...')
        except Exception as e:
            proceed(f'Não foi possível adicionar o usuário. Erro: {e}''\n''Tentando criar tabela. Tente novamente.')
            create_table()
        finally:
            cursor.close()
            con.close()
            break
    
    
def list_users(return_users=False):
    while True:
        try:
            con, cursor = get_connection()

            cursor.execute('select nome, email from tb_usuario;')
            users = cursor.fetchall()
            
            if (return_users == True):
                return None if (users == []) else users
            else:
                system('cls')
                for user in users:
                    print(f'Nome: {user[0]}, E-mail: {user[1]}')
                
                sleep(10)
                proceed('Retornando ao menu principal...')
                break
        except Exception as e:
            proceed(f'Não há nada para listar. Crie um usuário primeiro. Erro: {e}')
        finally:
            cursor.close()
            con.close()


def edit_user_info():
    while True:
        try:
            con, cursor = get_connection()
            exists, user_id = log_in()

            if exists == True:
                proceed('Usuário encontrado!')
                print('Menu de edição de usuário:')
                print('\n''1 - Editar nome')
                print('2 - Editar e-mail')
                print('3 - Editar senha')
                print('4 - Voltar ao menu principal')
                
                opt = input(' \n''Insira a ooperação que deseja realizar: ').strip()
                match opt:
                    case '1':
                        system('cls')
                        nome = input('Insira o novo nome do usuário: ')
                        cursor.execute('''
                                       update tb_usuario
                                       set nome = ?
                                       where id = ?;
                                       ''', 
                                       (nome, user_id))
                        con.commit()
                        
                    case '2':
                        system('cls')
                        email = get_email('Insira o novo email do usuário:')
                        cursor.execute('''
                                       update tb_usuario
                                       set email = ?
                                       where id = ?;
                                       ''', 
                                       (email, user_id))
                        con.commit()
                        
                    case '3':
                        system('cls')
                        senha = get_password(input('Insira a nova senha do usuário:'))
                        cursor.execute('''
                                       update tb_usuario
                                       set senha = ?
                                       where id = ?;
                                       ''', 
                                       (senha, user_id))
                        con.commit()
                    
                    case '4':
                        proceed('Retornando ao menu principal...')
                        break              
                        
                    case _:
                        proceed('Opção inválida. Tente novamente.')
                        continue
                
            else:
                proceed(f'Ocorreu um erro com o sistema. Tente novamente.')
                break
    
        except Exception as e:
            proceed(f'Não foi possível acessar o usuário. Erro: {e}')
            break

        finally:
            cursor.close()
            con.close()
            break


def delete_user():
    while True:
        try:
            con, cursor = get_connection()
            exists, user_id = log_in()
            
            if exists == True:
                system('cls')
                opt = (input('Tem certeza de que deseja prosseguir? (s/n): ').lower()).strip()
                
                if opt == 's':
                    cursor.execute('delete from tb_usuario where id = ?;', (user_id,))
                    con.commit()
                    proceed('Usuário exclúido com sucesso! Retornando ao menu principal.')
                elif opt == 'n':
                    proceed('Retornando ao menu principal...')
                else:
                    proceed('Opção inválida. Por favor, tente novamente.')
            else:
                proceed('O usuário fornecido não consta no banco de dados. Tente novamente.')
            
        except Exception as e:
            proceed(f'Não foi possível excluir o usuário. Erro: {e}')
            
        finally:
            cursor.close()
            con.close()
    

