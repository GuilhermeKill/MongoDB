from utils import config
from utils.splash_screen import SplashScreen
from reports.relatorios import Relatorio
from controller.controller_user import Controller_User
from controller.controller_movie_type import Controller_MovieType
from controller.controller_movie import Controller_Movie
from controller.controller_user_movie import Controller_User_movie

tela_inicial = SplashScreen()
relatorio = Relatorio()
ctrl_user = Controller_User()
ctrl_movie_type = Controller_MovieType()
ctrl_movie = Controller_Movie()
ctrl_user_movie = Controller_User_movie()

def reports(opcao_relatorio:int=0):
    if opcao_relatorio == 1:
        relatorio.get_relatorio_users()
    elif opcao_relatorio == 2:
        relatorio.get_relatorio_movies()
    elif opcao_relatorio == 3:
        relatorio.get_relatorio_movies_type()
    elif opcao_relatorio == 4:
        relatorio.get_relatorio_vendas()
    elif opcao_relatorio == 5:
        relatorio.get_relatorio_quantia_gasta()

def inserir(opcao_inserir:int=0):
    if opcao_inserir == 1:
        novo_user = ctrl_user.inserir_user()
    elif opcao_inserir == 2:
        novo_movie = ctrl_movie.inserir_movie()
    elif opcao_inserir == 3:
        novo_movie_type = ctrl_movie_type.inserir_movie_type()
    elif opcao_inserir == 4:
        novo_user_movie = ctrl_user_movie.inserir_user_movie()

def atualizar(opcao_atualizar:int=0):
    if opcao_atualizar == 1:
        user_atualizado = ctrl_user.atualizar_user()
    elif opcao_atualizar == 2:
        movie_atualizado = ctrl_movie.atualizar_movie()

def excluir(opcao_excluir:int=0):
    if opcao_excluir == 1:
        ctrl_movie_type.excluir_movie_type()

def run():
    print(tela_inicial.get_updated_screen())
    config.clear_console()

    while True:
        try:
            print(config.MENU_PRINCIPAL)
            opcao = int(input("Escolha uma opção [1-5]: "))
            config.clear_console(1)
            
            if opcao == 1: 
                
                print(config.MENU_RELATORIOS)
                opcao_relatorio = int(input("Escolha uma opção [0-6]: "))
                config.clear_console(1)

                reports(opcao_relatorio)

                config.clear_console(1)

            elif opcao == 2: 
                
                print(config.MENU_ENTIDADES)
                opcao_inserir = int(input("Escolha uma opção [1-5]: "))
                config.clear_console(1)

                inserir(opcao_inserir=opcao_inserir)
                
                while True:
                    print("Deseja continuar inserindo? [S / N]")
                    op = str(input()).upper()
                    if op == 'S':
                        inserir(opcao_inserir=opcao_inserir)
                    elif op == 'N': 
                        break
                    else:
                        print("opcção inválida")
                        break


                config.clear_console()
                print(tela_inicial.get_updated_screen())
                config.clear_console()

            elif opcao == 3: 

                print("O que deseja atualizar? \n 1 - Usuário \n 2 - Filme \n")
                opcao_atualizar = int(input("Escolha uma opção [1 - 2]: "))
                config.clear_console(1)

                atualizar(opcao_atualizar=opcao_atualizar)

                while True:
                    print("Deseja continuar atualizando? [S / N]")
                    op = str(input()).upper()
                    if op == 'S':
                        inserir(opcao_inserir=opcao_atualizar)
                    elif op == 'N': 
                        break
                    else:
                        print("opcção inválida")
                        break

                config.clear_console()

            elif opcao == 4:

                print("O que deseja exluir? \n 1 - Genero de filme \n")
                opcao_excluir = int(input("Escolha uma opção [1]: "))
                config.clear_console(1)

                excluir(opcao_excluir=opcao_excluir)
                
                while True:
                    print("Deseja continuar excluindo? [S / N]")
                    op = str(input()).upper()
                    if op == 'S':
                        inserir(opcao_inserir=opcao_excluir)
                    elif op == 'N': 
                        break
                    else:
                        print("opcção inválida")
                        break


                config.clear_console()
                print(tela_inicial.get_updated_screen())
                config.clear_console()

            elif opcao == 5:

                print(tela_inicial.get_updated_screen())
                config.clear_console()
                print("Obrigado por utilizar o nosso sistema.")
                exit(0)

            else:
                print("Opção incorreta.")
                exit(1)
        except ValueError:
            print("\n\nValor inválido\n\n")
        

if __name__ == "__main__":
    run()