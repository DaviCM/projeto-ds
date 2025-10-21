from user.user_services import *

def user_main():
    while True:
        users = list_users(return_users=True)

        if users == None:
            opt = (input('A lista de usuários está vazia. Deseja cadastrar um? (s/n): ').lower()).strip()
            if opt == 's':
                system('cls')
                create_user()
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
            print('Bem-vindo ao gerenciador de usuário com SQLite3!''\n')
            print('1 - Visualizar usuários cadastrados')
            print('2 - Cadastrar novo usuário')
            print('3 - Editar informações de um usuário')
            print('4 - Remover usuário')
            print('5 - Sair')
            opt = input('\n''Escolha o que deseja fazer: ').strip()

            match opt:
                case '1':
                    list_users()
                    continue

                # A partir daqui, chama a função certa para cada opção do user.
                case '2':
                    system('cls')
                    create_user()
                    continue
                case '3':
                    system('cls')
                    edit_user_info()
                    continue
                case '4':
                    system('cls')
                    delete_user()
                    continue
                case '5':
                    print('Adeus, amigo.')
                    break
                case _:
                    proceed('Opção inválida. Por favor, tente novamente.')
                    continue


