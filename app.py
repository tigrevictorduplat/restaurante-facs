from flask import Flask, jsonify, request
from crud import conectar_banco

app = Flask(__name__)


@app.route('/reservas', methods=['POST'])
def criar_reserva():
    dados = request.json

    def operacao(cursor):
        sql = """
            INSERT INTO tb_reservas 
            (dataReserva, horaReserva, nomeCliente, quatidadePessoas, statusReservaConfirmada, idMesaReserva)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores = (
            dados['dataReserva'],
            dados['horaReserva'],
            dados['nomeCliente'],
            dados['quatidadePessoas'],
            dados['statusReservaConfirmada'],
            dados['idMesaReserva']
        )
        cursor.execute(sql, valores)
        return cursor.lastrowid

    reserva_id = conectar_banco(operacao)

    return jsonify({'mensagem': 'Reserva criada', 'idReserva': reserva_id})


@app.route('/mesas', methods=['GET'])
def listar_mesas():
    def operacao(cursor):
        cursor.execute("SELECT * FROM tb_mesas")
        return cursor.fetchall()

    dados = conectar_banco(operacao)

    mesas = []
    for linha in dados:
        mesas.append({
            'idMesas': linha[0],
            'statusMesaOcupada': linha[1]
        })
    return jsonify(mesas)


@app.route('/reservas/<int:idReserva>', methods=['DELETE'])
def deletar_reserva(idReserva):
    def operacao(cursor):
        cursor.execute("DELETE FROM tb_reservas WHERE idReserva = %s", (idReserva,))
    conectar_banco(operacao)
    return jsonify({'mensagem': 'Reserva deletada com sucesso'})


if __name__ == '__main__':
    app.run(debug=True)
