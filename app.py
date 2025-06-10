import  atendente, garcom, gerente
from utils import separarLinha

if __name__ == "__main__":
    while True:
        print("\t\t===Restaurante FACS===\nSeja bem vindo, qual área do sistema deseja acessar?")
        separarLinha()
        print("1 - Atendente\n2 - Garçom\n3 - Gerente\n4 - Sair")
        act = int(input("Escolha uma opção: "))
        separarLinha()
        if act == 1:
            atendente.exibir_menu_atendente()
        elif act == 2:
            garcom.exibir_menu_garcom()
        elif act == 3:
            gerente.exibir_menu_gerente()
        elif act == 4:
            print("Saindo do sistema. Até mais!")
            break
        else:
            print("Opção inválida. Tente novamente.")
            separarLinha()