import requests
import json

API_URL = "http://localhost:5000"

def criar_reserva():
    data = {
        "dataReserva": input("digite a data da reserva (YYYY-MM-DD): \n"),
        "horaReserva": input("Digite o horário da reserva (HH:MM:SS): \n"),
        "idMesaReserva":int(input("Digite o número da mesa: \n")),
        "quantidadePessoas":int(input("Digite a quantidade de pessoas: \n")),
        "nomeCliente": input("Digite o nome do cliente: \n") 
    }
   
   
    try: 
        response =requests.post(f"{API_URL}/atendente/criar_reserva", json= data) 
        print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Erro ao realizar a requisição: {e}")



def cancelar_reserva():
    idReserva = int(input("Digite o id da reserva que deseja apagar: \n"))
   
    try:
        response = requests.delete(f"{API_URL}/atendente/apagar_reserva/{idReserva}")
        print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Erro ao realizar a requisição: {e}")