import requests
import json


API_URL = "http://localhost:5000"




def relatorio_reservas():
    response = requests.get(f"{API_URL}/gerente/relatorio_reservas")
    data_inicio = input("Insira a data de início da pesquisa: \n")
    data_fim = input("Insira a data de fim da pesquisa: \n")
    params = {
        "data_inicio": data_inicio,
        "data_fim": data_fim
    }
    response = requests.get(f"{API_URL}/gerente/relatorio_reservas", params=params)
    print(response.json())


def relatorio_por_mesa():
   idMesa = int(input("Digite o ID da mesa: \n"))
   response = requests.get(f"{API_URL}/gerente/relatorio_mesa/{idMesa}")
   print(response.json())
   

def mesas_confirmadas():
    response = requests.get(f"{API_URL}/gerente/relatorio_mesas_confirmadas")
    print(response.json())