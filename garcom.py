import requests
import json

# URL base da sua API Flask. Se estiver rodando no Replit, substitua por sua URL do Repl.
API_BASE_URL = "http://127.0.0.1:5000"

def _fazer_requisicao(method, endpoint, data=None, params=None):
    """Função auxiliar para fazer requisições HTTP e tratar respostas/erros."""
    response = None  # Inicializa response para evitar erro 'unbound'
    try:
        url = f"{API_BASE_URL}{endpoint}"
        if method == "PUT":
            response = requests.put(url, json=data)
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
            if response is not None:
                error_details = response.json()
                print(f"Detalhes do erro da API: {json.dumps(error_details, indent=2, ensure_ascii=False)}")
            else:
                print("Resposta não disponível para decodificação.")
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

def confirmar_reserva_garcom():
    """Coleta o ID da reserva e envia requisição para confirmá-la."""
    print("\n--- Confirmar Reserva ---")
    try:
        id_reserva = int(input("Digite o ID da reserva que deseja confirmar: "))
    except ValueError:
        print("Erro: O ID da reserva deve ser um número inteiro.")
        return

    _fazer_requisicao("PUT", f"/garcom/confirmar_reserva/{id_reserva}")

def exibir_menu_garcom():
    """Exibe o menu principal para o garçom."""
    while True:
        print("\n=== Painel do Garçom ===")
        print("1. Confirmar Reserva")
        print("2. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            confirmar_reserva_garcom()
        elif opcao == "2":
            print("Saindo do painel do garçom. Bom trabalho!")
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida (1 ou 2).")

if __name__ == "__main__":
    exibir_menu_garcom()