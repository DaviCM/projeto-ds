from product.product_services import *

def product_main():
    while True:
        users = list_products(return_products=True)

        if users == None:
            opt = (input('A lista de produtos está vazia. Deseja cadastrar um? (s/n): ').lower()).strip()
            if opt == 's':
                system('cls')
                create_product()
                continue
            elif opt == 'n':
                system('cls')
                print('Adeus, amigo.')
                break
            else:
                proceed('Opção inválida. Por favor, tente novamente')
                continue
        else:
            system('cls')
            print('Bem-vindo ao gerenciador de produtos com SQLite3!''\n')
            print('1 - Visualizar produtos cadastrados')
            print('2 - Cadastrar novo produto')
            print('3 - Editar informações de um produto')
            print('4 - Remover produto')
            print('5 - Sair')
            opt = input('\n''Escolha o que deseja fazer: ').strip()

            match opt:
                case '1':
                    list_products()
                    continue

                # A partir daqui, chama a função certa para cada opção do user.
                case '2':
                    system('cls')
                    create_product()
                    continue
                case '3':
                    system('cls')
                    edit_product_info()
                    continue
                case '4':
                    system('cls')
                    sell_product()
                    continue
                case '5':
                    print('Adeus, amigo.')
                    break
                case _:
                    proceed('Opção inválida. Por favor, tente novamente.')
                    continue


