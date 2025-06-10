import requests
import json
from datetime import datetime, time
from utils import separarLinha
# URL base da sua API Flask. Se estiver rodando no Replit, substitua por sua URL do Repl.
API_BASE_URL = "http://127.0.0.1:5000"

def _fazer_requisicao(method, endpoint, data=None, params=None):
    """Função auxiliar para fazer requisições HTTP e tratar respostas/erros."""
    response = None  # Inicializa response para evitar erro 'unbound'
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
        if endpoint.__contains__('/atendente/cancelar_reserva/'):
            print(f"\n{response_json.get('mensagem', 'Sem mensagem')}")
        elif endpoint.__contains__('/atendente/criar_reserva'):
            print(f"\n{response_json.get('mensagem', 'Sem mensagem')}\nID da reserva: {response_json.get('idReserva', 'N/A')}")


    except requests.exceptions.HTTPError as http_err:
        # print(f"\nErro HTTP: {http_err}")
        try:
            if response is not None:
                error_details = response.json()
                # print(f"Detalhes do erro da API: {json.dumps(error_details, indent=2, ensure_ascii=False)}")
                print(f"\n{error_details['erro']}")
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

def validar_e_formatar_data_hora(data_str, hora_str):
    """
    Valida e formata a data para YYYY-MM-DD e a hora para HH:MM:00.
    Permite input de data em DD/MM/YYYY ou YYYY-MM-DD.
    """
    # Tenta parsear a data nos formatos DD/MM/YYYY e YYYY-MM-DD
    data_obj = None
    try:
        data_obj = datetime.strptime(data_str, '%d/%m/%Y').date() # Tenta DD/MM/YYYY
    except ValueError:
        try:
            data_obj = datetime.strptime(data_str, '%Y-%m-%d').date() # Tenta YYYY-MM-DD
        except ValueError:
            print("\nErro de validação: Formato de data inválido. Use DD/MM/YYYY ou YYYY-MM-DD.")
            return None, None
            
    # Valida e formata a hora (ignorando segundos)
    hora_obj = None
    try:
        # Aceita HH:MM ou HH:MM:SS, e padroniza para HH:MM:00
        partes_hora = hora_str.split(':')
        if len(partes_hora) == 2:
            hora_obj = time(int(partes_hora[0]), int(partes_hora[1]), 0) # Adiciona 00 segundos
        elif len(partes_hora) == 3:
            hora_obj = time(int(partes_hora[0]), int(partes_hora[1]), int(partes_hora[2])) # Aceita HH:MM:SS
        else:
            raise ValueError
    except ValueError:
        print("\nErro de validação: Formato de hora inválido. Use HH:MM ou HH:MM:SS.")
        return None, None
    
    return data_obj.isoformat(), hora_obj.strftime('%H:%M:%S')

def criar_nova_reserva():
    """Coleta dados, valida e envia uma requisição para criar uma nova reserva."""
    print("\n--- Criar Nova Reserva ---")
    data_reserva_input = input("1. Digite a data da reserva (DD/MM/YYYY ou YYYY-MM-DD, ex: 31/12/2025): ")
    hora_reserva_input = input("2. Digite o horário da reserva (HH:MM ou HH:MM:SS, ex: 19:30): ")
    nome_cliente = input("3. Digite o nome do cliente: ")

    # Validação e formatação de data/hora
    data_reserva, hora_reserva = validar_e_formatar_data_hora(data_reserva_input, hora_reserva_input)
    if data_reserva is None or hora_reserva is None:
        return # Erro já foi impresso pela função de validação

    # Validações de campos vazios e numéricos
    if not nome_cliente.strip():
        print("Erro de validação: O nome do cliente não pode ser vazio.")
        return
    
    try:
        id_mesa_reserva = int(input("4. Digite o número da mesa (ex: 5): "))
        if id_mesa_reserva <= 0:
            print("Erro de validação: O número da mesa deve ser um número inteiro positivo.")
            return
        quantidade_pessoas = int(input("5. Digite a quantidade de pessoas (ex: 2): "))
        # A validação de range (0 < pessoas <= 20) será feita no servidor (app.py),
        # mas podemos adicionar uma pré-validação aqui para feedback rápido.
        if not (0 < quantidade_pessoas <= 20): # Usando 20 como limite Hardcoded no cliente por enquanto
             print("Erro de validação: A quantidade de pessoas deve ser maior que 0 e menor ou igual a 20.")
             return
    except ValueError:
        print("Erro de validação: O número da mesa e a quantidade de pessoas devem ser números inteiros válidos.")
        return

    payload = {
        "dataReserva": data_reserva,
        "horaReserva": hora_reserva,
        "nomeCliente": nome_cliente.strip(),
        "quantidadePessoas": quantidade_pessoas,
        "idMesaReserva": id_mesa_reserva
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
        separarLinha()

        if opcao == "1":
            criar_nova_reserva()
            separarLinha()
        elif opcao == "2":
            cancelar_reserva_existente()
            separarLinha()
        elif opcao == "3":
            print("Saindo do painel do atendente. Até mais!")
            separarLinha()
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida (1, 2 ou 3).")
            separarLinha()

if __name__ == "__main__":
    exibir_menu_atendente()