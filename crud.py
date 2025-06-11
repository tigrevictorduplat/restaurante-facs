import mysql.connector
import datetime
import os

def conectar_banco():
    return mysql.connector.connect(
        host=os.environ.get('DB_HOST', 'db'),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASSWORD', 'root'),
        database=os.environ.get('DB_NAME', 'banco_restaurante'),
    )

def criar_reserva_db(cursor, dataReserva, horaReserva, nomeCliente, quantidadePessoas, idMesaReserva):
    sql = "INSERT INTO tb_reservas (dataReserva, horaReserva, nomeCliente, quantidadePessoas, statusReservaConfirmada, idMesaReserva) VALUES (%s, %s, %s, %s, 0, %s)"
    cursor.execute(sql, (dataReserva, horaReserva, nomeCliente, quantidadePessoas, idMesaReserva))
    return cursor.lastrowid

# def verificar_disponibilidade_mesa_db(cursor, idMesaReserva, dataReserva, horaReserva):
#     """
#     Verifica se a mesa está disponível para reserva na data e hora especificadas.
#     Considera:
#     1. Se a mesa existe na tb_mesas.
#     2. Se a mesa não está marcada como 'ocupada' (statusMesaOcupada = 1).
#     3. Se não há outra reserva *confirmada* (statusReservaConfirmada = 1) para a mesma mesa na mesma data e hora.
#     """
#
#     # 1. Verificar se a mesa existe e seu status atual
#     sql_mesa = "SELECT statusMesaOcupada FROM tb_mesas WHERE idMesa = %s"
#     cursor.execute(sql_mesa, (idMesaReserva,))
#     mesa_info = cursor.fetchone()
#
#     if not mesa_info:
#         return {'disponivel': False, 'motivo': 'Mesa não encontrada.'}
#
#     status_mesa_ocupada = mesa_info[0]
#     if status_mesa_ocupada == 1:
#         return {'disponivel': False, 'motivo': 'Mesa está atualmente marcada como ocupada.'}
#
#     # 2. Verificar se já existe uma reserva (confirmada ou não) para aquela mesa na data e hora
#
#     sql_reserva_existente = "SELECT idReserva FROM tb_reservas WHERE idMesaReserva = %s AND dataReserva = %s AND horaReserva = %s"
#     cursor.execute(sql_reserva_existente, (idMesaReserva, dataReserva, horaReserva))
#     reserva_existente = cursor.fetchone()
#
#     if reserva_existente:
#         return {'disponivel': False, 'motivo': 'Já existe uma reserva para esta mesa, data e hora.'}
#
#     return {'disponivel': True}

def verificar_disponibilidade_mesa_db(cursor, idMesaReserva, dataReserva, horaReserva):
    """
    Verifica se a mesa está disponível para reserva na data e hora especificadas.
    Considera:
    1. Se a mesa existe na tb_mesas.
    2. Se a mesa não está marcada como 'ocupada' (statusMesaOcupada = 1).
    3. Se não há outra reserva *confirmada* (statusReservaConfirmada = 1) para a mesma mesa na mesma data e hora.
    4. Se não há outra reserva dentro do intervalo de 2 horas antes ou depois.
    """

    # 1. Verificar se a mesa existe e seu status atual
    sql_mesa = "SELECT statusMesaOcupada FROM tb_mesas WHERE idMesa = %s"
    cursor.execute(sql_mesa, (idMesaReserva,))
    mesa_info = cursor.fetchone()

    if not mesa_info:
        return {'disponivel': False, 'motivo': 'Mesa não encontrada.'}

    status_mesa_ocupada = mesa_info[0]
    if status_mesa_ocupada == 1:
        return {'disponivel': False, 'motivo': 'Mesa está atualmente marcada como ocupada.'}

    # 2. Verificar se já existe uma reserva (confirmada ou não) para aquela mesa na data e hora
    sql_reserva_existente = "SELECT idReserva FROM tb_reservas WHERE idMesaReserva = %s AND dataReserva = %s AND horaReserva = %s"
    cursor.execute(sql_reserva_existente, (idMesaReserva, dataReserva, horaReserva))
    reserva_existente = cursor.fetchone()

    if reserva_existente:
        return {'disponivel': False, 'motivo': 'Já existe uma reserva para esta mesa, data e hora.'}

    # 3. Verificar se há reservas dentro do intervalo de 2 horas antes ou depois
    dt_reserva = datetime.datetime.combine(dataReserva, horaReserva)

    # Calcular 2 horas antes e depois
    dt_inicio = (dt_reserva - datetime.timedelta(hours=2))
    dt_fim = (dt_reserva + datetime.timedelta(hours=2))

    # Verificar se há reservas no intervalo
    sql_intervalo = """
        SELECT idReserva FROM tb_reservas
        WHERE idMesaReserva = %s
        AND dataReserva = %s
        AND (
            TIME_TO_SEC(horaReserva) BETWEEN TIME_TO_SEC(%s) AND TIME_TO_SEC(%s)
            OR
            ABS(TIME_TO_SEC(horaReserva) - TIME_TO_SEC(%s)) <= 7200
        )
        """
    cursor.execute(sql_intervalo,
                   (idMesaReserva, dataReserva, dt_inicio.strftime('%H:%M:%S'), dt_fim.strftime('%H:%M:%S'),
                    horaReserva))

    # Imprimir para debug
    print(f"Verificando reservas para mesa {idMesaReserva} em {dataReserva} entre {dt_inicio} e {dt_fim}")
    print(f"SQL: {sql_intervalo}")
    print(
        f"Parâmetros: {idMesaReserva}, {dataReserva}, {dt_inicio.strftime('%H:%M:%S')}, {dt_fim.strftime('%H:%M:%S')}, {horaReserva}")

    reservas_intervalo = cursor.fetchall()
    print(f"Reservas encontradas: {reservas_intervalo}")

    if reservas_intervalo:
        return {'disponivel': False, 'motivo': 'Já existe uma reserva para esta mesa dentro do intervalo de 2 horas.'}

    return {'disponivel': True}


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
verificar_disponibilidade_mesa = executar_query(verificar_disponibilidade_mesa_db)
cancelar_reserva = executar_query(cancelar_reserva_db)
confirmar_reserva = executar_query(confirmar_reserva_db)
obter_relatorio_reservas_periodo_status = executar_query(obter_relatorio_reservas_por_periodo_status_db)
obter_reservas_por_mesa_relatorio = executar_query(obter_reservas_por_mesa_relatorio_db)
obter_mesas_confirmadas_relatorio = executar_query(obter_mesas_confirmadas_relatorio_db)