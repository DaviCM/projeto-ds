from connection import get_connection
from services.proceed import *
from decimal import Decimal

def get_decimal(message):
    while True:
        try:
            value = Decimal((input(message).replace(',', '.')).strip())
            return value
        except ValueError:
            proceed('Valor inválido. Por favor, tente novamente.')
            continue
        

def get_int(message, proceeded=True):
    while True:
        try:
            value = int(input(message).strip())
            return value
        except ValueError:
            proceed('Valor inválido. inválida. Tente novamente.') if proceeded == True else ...
            continue
        

def create_table():
    try:
        con, cursor = get_connection() # Cursor Rodará os comandos, como o cursor do CMD
        cursor.execute(
            # Auto increment no sqlite3 é automático em primary key
            # Tipo decimal em sql é similar ao float, porém mais preciso
            '''
            create table if not exists tb_produto(
                
                id integer primary key, 
                desc varchar(120) not null,
                valor decimal not null,
                qtd integer check (qtd > 0)
            );     
            '''
        )
        proceed('Tabela criada com sucesso!')
    except Exception as e:
        proceed(f'Não foi possível criar a tabela. Erro: {e}')
    finally:
        cursor.close()
        con.close()
        

def create_product():
    try:
        con, cursor = get_connection() # Cursor Rodará os comandos, como o cursor do CMD
        
        desc = (input('Digite o nome do novo produto: ').title()).strip()
        valor = get_decimal('Digite o valor do produto: R$')
        qtd = get_int('Digite a quantidade disponível desse produto: ')
        
        cursor.execute('insert into tb_produto(desc, valor, qtd) values(?, ?, ?);', (desc, valor, qtd))
        con.commit()
    except Exception as e:
        proceed(f'Não foi possível adicionar o produto. Erro: {e}''\n''Tentando criar tabela. Tente novamente.')
        create_table()
    finally:
        cursor.close()
        con.close()
    

def list_products(return_products=False, proceeded=True, id=None):
    while True:
        try:
            con, cursor = get_connection()

            cursor.execute('select * from tb_produto;')
            products = cursor.fetchall()
            
            system('cls')
            
            if (return_products == True):
                return None if (products == []) else products
            
            for item in products:
                print(f'ID: {item[0]}')
                print(f'Nome do produto: {item[1]}')
                print(f'Valor do produto: R${item[2]}')
                print(f'Quantidade em estoque: {item[3]}')
            
            sleep(10)
            proceed('Retornando ao menu principal...') if proceeded == True else ...
            break
        except Exception as e:
            proceed(f'Não há nada para listar. Cadastre um produto primeiro. Erro: {e}')
        finally:
            cursor.close()
            con.close()


def get_product_qtd(id):
    while True:
        try:
            con, cursor = get_connection()
            cursor.execute('select desc, qtd from tb_produto where id = ?;', (id,))
            product_quantity = cursor.fetchall()
            return product_quantity if product_quantity[1] != 0 else (None, None)
        except Exception as e:
            proceed(f'Não há nada para listar. Cadastre um produto primeiro. Erro: {e}')
        finally:
            cursor.close()
            con.close()
                        

def edit_product_info():
    while True:
        try:
            con, cursor = get_connection()
            
            list_products(proceeded=False)
            product_id = get_int('Insira o ID do produto que deseja deletar: ', proceeded=False)

            print('Menu de edição de produto:')
            print('\n''1 - Editar nome')
            print('2 - Editar preço')
            print('3 - Editar quantidade')
            print('4 - Voltar ao menu principal')
            
            opt = input(' \n''Insira a ooperação que deseja realizar: ').strip()
            match opt:
                case '1':
                    system('cls')
                    desc = (input('Insira o novo nome do produto:').title()).strip()
                    cursor.execute('''
                                   update tb_produto
                                   set desc = ?
                                   where id = ?;
                                   ''', 
                                   (desc, product_id))
                    con.commit()
                    
                case '2':
                    system('cls')
                    valor = get_decimal('Insira o novo valor do produto: R$')
                    cursor.execute('''
                                   update tb_produto
                                   set valor = ?
                                   where id = ?;
                                   ''', 
                                   (valor, product_id))
                    con.commit()
                    
                case '3':
                    system('cls')
                    qtd = get_int('Insira a nova quantidade disponível:')
                    cursor.execute('''
                                   update tb_produto
                                   set qtd = ?
                                   where id = ?;
                                   ''', 
                                   (qtd, product_id))
                    con.commit()
                    
                case '4':
                    proceed('Retornando ao menu principal...')
                    break      
                        
                case _:
                    proceed('Opção inválida. Tente novamente.')
                    continue
        except Exception as e:
            proceed(f'Não foi possível acessar o usuário. Erro: {e}')
            break
        finally:
            cursor.close()
            con.close()
            break
        

def sell_product():
    while True:
        try:
            con, cursor = get_connection()
            
            list_products(proceeded=False)
            
            product_id = get_int('Insira o ID do produto que deseja vender: ', proceeded=False)
            
            try:
                desc, qtd = get_product_qtd(return_products=True, id=product_id)
            except ValueError:
                proceed('O produto está com quantidade 0. Adicione uma quantidade antes de vender.')
                proceed('Retornando ao menu principal...')
                break
            
            print(f'QTD de {desc} disponível: {qtd} unidades')
            to_sell = get_int('Insira a quantidade que deseja vender:')
            
            if to_sell > qtd:
                proceed(f'Há apenas {qtd} produtos em estoque. Por favor, insira um valor válido.')
                continue
            
            system('cls')
            opt = (input('Tem certeza de que deseja prosseguir? (s/n): ').lower()).strip()
            
            if opt == 's':
                new_qtd = qtd - to_sell
                cursor.execute('''
                               update tb_produto 
                               set qtd = qtd - ?
                               where id = ?;
                               ''',
                               (new_qtd, product_id))
                con.commit()
                proceed('Produto vendido com sucesso! Retornando ao menu principal.')
            elif opt == 'n':
                proceed('Retornando ao menu principal...')
            else:
                proceed('Opção inválida. Por favor, tente novamente.')
            
        except Exception as e:
            proceed(f'Não foi possível excluir o produto. Erro: {e}')
            
        finally:
            cursor.close()
            con.close()
            


            
