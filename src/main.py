from user.user_services import log_in
from user.user_main import user_main
from product.product_main import product_main
from proceed import *

def main():
    while True:
        proceed('Faça login com seu usuário e sua senha!')
        username, user_email = log_in(get_user=True)

        system('cls')
        print('Bem-vindo ao gerenciador de usuário com SQLite3!')
        print(f'Você está logado como: {username} <{user_email}>''\n')
        print('1 - Acessar menu de usuários')
        print('2 - Acessar menu de produtos')
        print('3 - Sair')
        opt = input('\n''Escolha o que deseja fazer: ').strip()
        match opt:
            case '1':
                system('cls')
                user_main()
                continue
            case '2':
                system('cls')
                product_main()
                continue
            case '3':
                print('Adeus, amigo.')
                break
            case _:
                proceed('Opção inválida. Por favor, tente novamente.')
                continue


if __name__ == '__main__':
    main()



