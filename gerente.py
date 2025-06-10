import requests
import json
from datetime import datetime
from utils import separarLinha

# URL base da sua API Flask. Se estiver rodando no Replit, substitua por sua URL do Repl.
API_BASE_URL = "http://127.0.0.1:5000"

def _fazer_requisicao_get(endpoint, params=None):
    """Função auxiliar para fazer requisições GET e tratar respostas/erros."""
    response = None  # Inicializa response para evitar erro 'unbound'
    try:
        url = f"{API_BASE_URL}{endpoint}"
        response = requests.get(url, params=params)

        response.raise_for_status() # Levanta um HTTPError para códigos de status de erro (4xx ou 5xx)
        response_json = response.json()

        # Formata a saída JSON de forma mais legível
        if endpoint.__contains__("/gerente/relatorio_mesa/"):
            try:
                for i, item in enumerate(response_json):
                    if item['statusReservaConfirmada'] == 1:
                        status = "Confirmada"
                    else:
                        status = "Não confirmada"
                    print(f"Reserva {i+1}")
                    separarLinha()
                    print(f"ID da Reserva: {item['idReserva']}\nMesa: {item['idMesaReserva']}\nData e Hora: {item['dataReserva']} / {item['horaReserva']}\nCliente: {item['nomeCliente']}\nQuantidade de pessoas: {item['quantidadePessoas']} Pessoa(s)\nStatus da Reserva: {status}")
                    separarLinha()
            except Exception:
                separarLinha()
                print(f"Não há reservas para esta mesa ou não existe mesa com este ID")
        elif endpoint.__contains__('/gerente/relatorio_mesas_confirmadas'):
            if isinstance(response_json, dict) and 'mensagem' in response_json:
                separarLinha()
                print(response_json.get('mensagem', 'Sem mensagem'))
                return
            for item in response_json:
                if type(item[0]) != int:
                    separarLinha()
                    print(f"Não há reservas confirmadas")
                    return
                idMesa = item[0]
                qtdReservas = item[1]
                print(f"Mesa {idMesa} possui {qtdReservas} reserva(s) confirmada(s)")
        elif endpoint.__contains__('/gerente/relatorio_reservas'):
            if isinstance(response_json, dict) and 'mensagem' in response_json:
                separarLinha()
                print(response_json.get('mensagem', 'Sem mensagem'))
                return
            for item in response_json:
                dataReserva = item[0]
                status = "Confirmada" if item[1] == 1 else "Não confirmada"
                total = item[2]
                print(f"\nData: {datetime.strptime(dataReserva, '%a, %d %b %Y %H:%M:%S GMT').strftime('%d/%m/%Y')} | Status: {status} | Total de reservas: {total}")

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

def relatorio_reservas_por_periodo_status():
    """Solicita um relatório de reservas por período e status."""
    print("\n--- Relatório de Reservas por Período e Status ---")
    data_inicio = input("1. Insira a data de início da pesquisa (YYYY-MM-DD): ")
    data_fim = input("2. Insira a data de fim da pesquisa (YYYY-MM-DD): ")
    try:
        # Converte as strings para objetos datetime
        dt_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
        dt_fim = datetime.strptime(data_fim, '%Y-%m-%d')

        # Verifica se a data de início é anterior à data de fim
        if dt_inicio > dt_fim:
            print("\nNão foi possível realizar a busca, a data de início deve ser anterior à data de fim.")
            return

        params = {
            "data_inicio": data_inicio,
            "data_fim": data_fim
        }

        _fazer_requisicao_get("/gerente/relatorio_reservas", params=params)
    except ValueError:
        print("Erro: Formato de data inválido. Use o formato YYYY-MM-DD.")

def relatorio_reservas_por_mesa():
    """Solicita um relatório de reservas para uma mesa específica."""
    print("\n--- Relatório de Reservas por Mesa ---")
    try:
        id_mesa = int(input("Digite o ID da mesa para o relatório: "))
    except ValueError:
        print("Erro: O ID da mesa deve ser um número inteiro.")
        return

    _fazer_requisicao_get(f"/gerente/relatorio_mesa/{id_mesa}")

def relatorio_mesas_confirmadas():
    """Solicita um relatório de todas as mesas que tiveram reservas confirmadas."""
    print("\n--- Relatório de Mesas com Reservas Confirmadas ---")
    _fazer_requisicao_get("/gerente/relatorio_mesas_confirmadas")

def exibir_menu_gerente():
    """Exibe o menu principal para o gerente."""
    while True:
        print("\n=== Painel do Gerente ===")
        print("1. Relatório de Reservas por Período e Status")
        print("2. Relatório de Reservas por Mesa")
        print("3. Relatório de Mesas com Reservas Confirmadas")
        print("4. Sair")

        opcao = input("Escolha uma opção: ")
        separarLinha()

        if opcao == "1":
            relatorio_reservas_por_periodo_status()
            separarLinha()
        elif opcao == "2":
            relatorio_reservas_por_mesa()
        elif opcao == "3":
            relatorio_mesas_confirmadas()
            separarLinha()
        elif opcao == "4":
            print("Saindo do painel do gerente. Tenha um bom dia!")
            separarLinha()
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida (1, 2, 3 ou 4).")
            separarLinha()

if __name__ == "__main__":
    exibir_menu_gerente()