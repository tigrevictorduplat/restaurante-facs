from flask import Flask, jsonify, request
# Importando o módulo de configuração para obter informações do restaurante
from config import RESTAURANT_INFO
# Importando as funções CRUD do módulo crud.py
from crud import criar_reserva, verificar_disponibilidade_mesa, cancelar_reserva, confirmar_reserva, obter_relatorio_reservas_periodo_status, obter_reservas_por_mesa_relatorio, obter_mesas_confirmadas_relatorio
# Importando o módulo datetime para manipulação de datas
import datetime 

app = Flask(__name__)

# --------- @route/atendente/criar_reserva --------- #
@app.route('/atendente/criar_reserva', methods=['POST'])
def criar_nova_reserva():
    data = request.get_json()
    dataReserva_str = data.get('dataReserva')
    horaReserva_str = data.get('horaReserva')
    nomeCliente = data.get('nomeCliente')
    quantidadePessoas = data.get('quantidadePessoas')
    idMesaReserva = data.get('idMesaReserva')

    # Validação 1: Campos obrigatórios
    if not all([dataReserva_str, horaReserva_str, idMesaReserva, quantidadePessoas, nomeCliente]):
        return jsonify({'erro': 'Todos os campos são obrigatórios'}), 400

    # Validação 2: Formato de Data/Hora e conversão para objeto date/time
    try:
        dataReserva = datetime.datetime.strptime(dataReserva_str, '%Y-%m-%d').date()
        horaReserva = datetime.datetime.strptime(horaReserva_str, '%H:%M:%S').time()
    except ValueError:
        return jsonify({'erro': 'Formato de data ou hora inválido. Use YYYY-MM-DD e HH:MM:SS.'}), 400

    # Validação 3: Impedir reservas para dias passados
    data_hoje = datetime.date.today()
    if dataReserva < data_hoje:
        return jsonify({'erro': 'Não é possível fazer reservas para datas no passado.'}), 400
    
    # Validação 4: Dias de funcionamento do restaurante
    dia_semana = dataReserva.weekday() # 0 = Segunda, 6 = Domingo
    # Verificar se o dia não está em dias_nao_funcionamento,
    # ou se a lista de dias_funcionamento não contém o dia atual
    if dia_semana in RESTAURANT_INFO.get("dias_nao_funcionamento", []): # Usar .get para segurança
        return jsonify({'erro': 'O restaurante não funciona neste dia da semana.'}), 400
    if RESTAURANT_INFO.get("dias_funcionamento"): # Só valida se a lista não for vazia
        if dia_semana not in RESTAURANT_INFO["dias_funcionamento"]:
            return jsonify({'erro': 'O restaurante não funciona neste dia da semana.'}), 400

    # Validação 5: Horário de funcionamento do restaurante
    horario_abertura = datetime.datetime.strptime(RESTAURANT_INFO["horario_abertura"], '%H:%M:%S').time()
    horario_fechamento = datetime.datetime.strptime(RESTAURANT_INFO["horario_fechamento"], '%H:%M:%S').time()
    
    # Se a reserva for para HOJE, precisamos verificar também se a hora já passou
    if dataReserva == data_hoje:
        hora_atual = datetime.datetime.now().time()
        if horaReserva < hora_atual:
            return jsonify({'erro': 'Não é possível fazer reservas para um horário que já passou hoje.'}), 400

    if not (horario_abertura <= horaReserva <= horario_fechamento):
        return jsonify({'erro': f'Horário de reserva fora do horário de funcionamento do restaurante ({RESTAURANT_INFO["horario_abertura"]} às {RESTAURANT_INFO["horario_fechamento"]}).'}), 400

    # Validação 6: Quantidade de pessoas 
    if not (0 < quantidadePessoas <= RESTAURANT_INFO["capacidade_maxima_mesa"]):
        return jsonify({'erro': f'A quantidade de pessoas deve ser maior que zero e menor ou igual a {RESTAURANT_INFO["capacidade_maxima_mesa"]} por mesa.'}), 400
    
    # Validação 7: Disponibilidade da mesa 
    status_mesa = verificar_disponibilidade_mesa(idMesaReserva, dataReserva, horaReserva)
    if not status_mesa['disponivel']:
        return jsonify({'erro': status_mesa['motivo']}), 409 # 409 Conflict

    # Se todas as validações passarem, cria a reserva
    try:
        reserva_id = criar_reserva(dataReserva, horaReserva, nomeCliente, quantidadePessoas, idMesaReserva)
        return jsonify({'mensagem': 'Reserva criada com sucesso', 'idReserva': reserva_id}), 201
    except Exception as e:
        return jsonify({'erro': f'Erro interno ao criar reserva: {str(e)}'}), 500

# ------------- @route/atendente/cancelar_reserva ---------------------- #
@app.route('/atendente/cancelar_reserva/<int:idReserva>', methods=['DELETE'])
def cancelar_reserva_rota(idReserva):
    registros_afetados = cancelar_reserva(idReserva)
    if registros_afetados > 0:
        return jsonify({'mensagem': f'Reserva com ID {idReserva} cancelada com sucesso'}), 200
    else:
        return jsonify({'erro': f'Reserva com ID {idReserva} não encontrada'}), 404

# ------------- @route/garçom/confirmar_reserva ------------ #
@app.route('/garcom/confirmar_reserva/<int:idReserva>', methods=['PUT'])
def confirmar_reserva_rota(idReserva):
    registros_afetados = confirmar_reserva(idReserva)
    if registros_afetados > 0:
        return jsonify({'mensagem': f'Reserva com ID {idReserva} confirmada com sucesso'}), 200
    else:
        return jsonify({'erro': f'Reserva com ID {idReserva} não encontrada ou já confirmada'}), 404

# ------------- @route/gerente/relatorio_reservas_atendidas ------------ #
@app.route('/gerente/relatorio_reservas', methods=['GET'])
def relatorio_reservas_periodo():
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')

    if not data_inicio or not data_fim:
        return jsonify({'erro': 'Os parâmetros data_inicio e data_fim são obrigatórios'}), 400

    relatorio = obter_relatorio_reservas_periodo_status(data_inicio, data_fim)
    return jsonify(relatorio), 200

# ------------- @route/gerente/relatorio_reservas_por_mesa ------------ #
@app.route('/gerente/relatorio_mesa/<int:idMesa>', methods=['GET'])
def relatorio_reservas_mesa(idMesa):
    relatorio = obter_reservas_por_mesa_relatorio(idMesa)
    if relatorio:
        return jsonify(relatorio), 200
    else:
        return jsonify({'mensagem': f'Não há reservas para a mesa {idMesa}'}), 200

# ------------- @route/gerente/relatorio_mesas_confirmadas------------ #
@app.route('/gerente/relatorio_mesas_confirmadas', methods=['GET'])
def relatorio_mesas_confirmadas():
    relatorio = obter_mesas_confirmadas_relatorio()
    if relatorio:
        return jsonify(relatorio), 200
    else:
        return jsonify({'mensagem': 'Não há mesas com reservas confirmadas'}), 200

if __name__ == '__main__':
    app.run(debug=True  )    