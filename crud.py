import mysql.connector
import datetime

def conectar_banco():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='banco_restaurante',
    )

def criar_reserva_db(cursor, dataReserva, horaReserva, nomeCliente, quantidadePessoas, idMesaReserva):
    sql = "INSERT INTO tb_reservas (dataReserva, horaReserva, nomeCliente, quantidadePessoas, statusReservaConfirmada, idMesaReserva) VALUES (%s, %s, %s, %s, 0, %s)"
    cursor.execute(sql, (dataReserva, horaReserva, nomeCliente, quantidadePessoas, idMesaReserva))
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
    sql = "SELECT idReserva, dataReserva, horaReserva, idMesaReserva, nomeCliente, quantidadePessoas, statusReservaConfirmada FROM vw_reservas_por_mesa WHERE idMesaReserva = %s"
    cursor.execute(sql, (idMesa,))
    
    # Obter os nomes das colunas para criar dicionários mais úteis
    # Isso é bom para JSON, pois os dicionários são mais fáceis de consumir do que tuplas
    colunas = [i[0] for i in cursor.description]
    resultados = []
    for linha in cursor.fetchall():
        registro = {}
        for i, valor in enumerate(linha):
            if isinstance(valor, (datetime.date, datetime.datetime)):
                registro[colunas[i]] = valor.isoformat() # Converte data/datetime para string ISO
            elif isinstance(valor, datetime.timedelta):
                # Formata timedelta para string HH:MM:SS
                total_seconds = int(valor.total_seconds())
                hours, remainder = divmod(total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                registro[colunas[i]] = f"{hours:02}:{minutes:02}:{seconds:02}"
            else:
                registro[colunas[i]] = valor
        resultados.append(registro)
        
    return resultados

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