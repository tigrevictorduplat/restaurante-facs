import mysql.connector

def conectar_banco():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='banco_restaurante',
    )

def criar_reserva_db(cursor, dataReserva, horaReserva, idMesaReserva, quantidadePessoas, nomeCliente):
    sql = "INSERT INTO tb_reservas (dataReserva, horaReserva, idMesaReserva, nomeCliente, quantidadePessoas, statusReservaConfirmada) VALUES (%s, %s, %s, %s, %s, 0)"
    cursor.execute(sql, (dataReserva, horaReserva, idMesaReserva, nomeCliente, quantidadePessoas, 0))
    return cursor.lastrowid

def verificar_mesa_reservada_db(cursor, idMesaReserva, dataReserva, horaReserva):
    sql = "SELECT idReserva FROM tb_reservas WHERE idMesaReserva = %s AND dataReserva = %s AND horaReserva = %s"
    cursor.execute(sql, (idMesaReserva, dataReserva, horaReserva))
    return cursor.fetchone()

def cancelar_reserva_db(cursor, idReserva):
    sql = "DELETE FROM tb_reservas WHERE idReserva = %s"
    cursor.execute(sql, (idReserva,))
    return cursor.rowcount

def confirmar_reserva_db(cursor, idReserva):
    sql = "UPDATE tb_reservas SET statusReservaConfirmada = 1 WHERE idReserva = %s AND statusReservaConfirmada = 0"
    cursor.execute(sql, (idReserva,))
    return cursor.rowcount

def obter_relatorio_reservas_por_periodo_status_db(cursor, data_inicio, data_fim):
    sql = "SELECT dataReserva, statusReservaConfirmada, totalReservas FROM vw_reservas_por_data_e_status WHERE dataReserva BETWEEN %s AND %s"
    cursor.execute(sql, (data_inicio, data_fim))
    return cursor.fetchall()

def obter_reservas_por_mesa_relatorio_db(cursor, idMesa):
    sql = "SELECT * FROM vw_reservas_por_mesa WHERE idMesaReserva = %s"
    cursor.execute(sql, (idMesa,))
    return cursor.fetchall()

def obter_mesas_confirmadas_relatorio_db(cursor):
    sql = "SELECT idMesa, totalConfirmacoes FROM vw_confirmacoes_por_mesa"
    cursor.execute(sql)
    return cursor.fetchall()

def executar_query(operacao):
    def wrapper(*args, **kwargs):
        conexao = conectar_banco()
        cursor = conexao.cursor()
        resultado = None
        try:
            resultado = operacao(cursor, *args, **kwargs)
            conexao.commit()
            return resultado
        except Exception as e:
            conexao.rollback()
            print(f"Erro ao executar operação '{operacao.__name__}': {e}")
            raise
        finally:
            cursor.close()
            conexao.close()
    return wrapper

criar_reserva = executar_query(criar_reserva_db)
verificar_mesa_reservada = executar_query(verificar_mesa_reservada_db)
cancelar_reserva = executar_query(cancelar_reserva_db)
confirmar_reserva = executar_query(confirmar_reserva_db)
obter_relatorio_reservas_periodo_status = executar_query(obter_relatorio_reservas_por_periodo_status_db)
obter_reservas_por_mesa_relatorio = executar_query(obter_reservas_por_mesa_relatorio_db)
obter_mesas_confirmadas_relatorio = executar_query(obter_mesas_confirmadas_relatorio_db)