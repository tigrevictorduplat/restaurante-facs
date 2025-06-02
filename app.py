from flask import Flask, jsonify, request
from crud import criar_reserva, verificar_mesa_reservada, cancelar_reserva, confirmar_reserva, obter_relatorio_reservas_periodo_status, obter_reservas_por_mesa_relatorio, obter_mesas_confirmadas_relatorio

app = Flask(__name__)

# --------- @route/atendente/criar_reserva --------- #
@app.route('/atendente/criar_reserva', methods=['POST'])
def criar_nova_reserva():
    data = request.get_json()
    dataReserva = data.get('dataReserva')
    horaReserva = data.get('horaReserva')
    idMesaReserva = data.get('idMesaReserva')
    quantidadePessoas = data.get('quantidadePessoas')
    nomeCliente = data.get('nomeCliente')

    if not all([dataReserva, horaReserva, idMesaReserva, quantidadePessoas, nomeCliente]):
        return jsonify({'erro': 'Todos os campos são obrigatórios'}), 400

    mesa_reservada = verificar_mesa_reservada(idMesaReserva, dataReserva, horaReserva)
    if mesa_reservada:
        return jsonify({'erro': 'Mesa já reservada para esta data e hora'}), 409

    reserva_id = criar_reserva(dataReserva, horaReserva, idMesaReserva, quantidadePessoas, nomeCliente)
    return jsonify({'mensagem': 'Reserva criada com sucesso', 'idReserva': reserva_id}), 201

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
    app.run(host='0.0.0.0', port=5000)    