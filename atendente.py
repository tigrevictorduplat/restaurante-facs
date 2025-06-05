import requests
import json

# URL base da sua API Flask. Se estiver rodando no Replit, substitua por sua URL do Repl.
API_BASE_URL = "http://127.0.0.1:5000"

def _fazer_requisicao(method, endpoint, data=None, params=None):
    """Função auxiliar para fazer requisições HTTP e tratar respostas/erros."""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        if method == "POST":
            response = requests.post(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        else:
            raise ValueError(f"Método HTTP '{method}' não suportado por esta função auxiliar.")

        response.raise_for_status() # Levanta um HTTPError para códigos de status de erro (4xx ou 5xx)
        response_json = response.json()

        # Formata a saída JSON de forma mais legível
        print("\n--- Resposta da API ---")
        print(json.dumps(response_json, indent=2, ensure_ascii=False))
        print("---------------------\n")

    except requests.exceptions.HTTPError as http_err:
        print(f"\nErro HTTP: {http_err}")
        try:
            error_details = response.json()
            print(f"Detalhes do erro da API: {json.dumps(error_details, indent=2, ensure_ascii=False)}")
        except json.JSONDecodeError:
            print("Não foi possível decodificar a resposta de erro como JSON.")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"\nErro de Conexão: Não foi possível conectar à API. Verifique se o servidor está rodando. {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"\nErro de Timeout: A requisição demorou muito para responder. {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"\nOcorreu um erro inesperado na requisição: {req_err}")
    except ValueError as val_err:
        print(f"\nErro de Validação interna: {val_err}")

def criar_nova_reserva():
    """Coleta dados e envia uma requisição para criar uma nova reserva."""
    print("\n--- Criar Nova Reserva ---")
    data_reserva = input("1. Digite a data da reserva (YYYY-MM-DD, ex: 2025-12-31): ")
    hora_reserva = input("2. Digite o horário da reserva (HH:MM:SS, ex: 19:30:00): ")

    try:
        id_mesa_reserva = int(input("3. Digite o número da mesa: "))
        quantidade_pessoas = int(input("4. Digite a quantidade de pessoas: "))
    except ValueError:
        print("Erro: O número da mesa e a quantidade de pessoas devem ser números inteiros.")
        return

    nome_cliente = input("5. Digite o nome do cliente: ")

    payload = {
        "dataReserva": data_reserva,
        "horaReserva": hora_reserva,
        "idMesaReserva": id_mesa_reserva,
        "quantidadePessoas": quantidade_pessoas,
        "nomeCliente": nome_cliente 
    }

    _fazer_requisicao("POST", "/atendente/criar_reserva", data=payload)

def cancelar_reserva_existente():
    """Coleta o ID e envia uma requisição para cancelar uma reserva."""
    print("\n--- Cancelar Reserva Existente ---")
    try:
        id_reserva = int(input("Digite o ID da reserva que deseja cancelar: "))
    except ValueError:
        print("Erro: O ID da reserva deve ser um número inteiro.")
        return

    _fazer_requisicao("DELETE", f"/atendente/cancelar_reserva/{id_reserva}")

def exibir_menu_atendente():
    """Exibe o menu principal para o atendente."""
    while True:
        print("\n=== Painel do Atendente ===")
        print("1. Criar Nova Reserva")
        print("2. Cancelar Reserva Existente")
        print("3. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            criar_nova_reserva()
        elif opcao == "2":
            cancelar_reserva_existente()
        elif opcao == "3":
            print("Saindo do painel do atendente. Até mais!")
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida (1, 2 ou 3).")

if __name__ == "__main__":
    exibir_menu_atendente()