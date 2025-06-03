import requests
import json

API_URL = "http:localhost://5000"

def confirmar_reserva():
    reservaId = input("Digite o Id da reservar que quer confirmar: \n")
    response = requests.put(f"{API_URL}/garcom/confirmar_reserva/{reservaId}")
    print(response.json())