import mysql.connector
import datetime
import os

def conectar_banco():
    """
    Realiza a conexão com o banco de dados MySQL usando variáveis de ambiente para configuração.
    """
    return mysql.connector.connect(
        host=os.environ.get('DB_HOST', 'db'),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASSWORD', 'root'),
        database=os.environ.get('DB_NAME', 'banco_restaurante'),
    )

def criar_reserva_db(cursor, dataReserva, horaReserva, nomeCliente, quantidadePessoas, idMesaReserva):
    """
    Insere uma nova reserva na tabela tb_reservas.
    """
    sql = "INSERT INTO tb_reservas (dataReserva, horaReserva, nomeCliente, quantidadePessoas, statusReservaConfirmada, idMesaReserva) VALUES (%s, %s, %s, %s, 0, %s)"
    cursor.execute(sql, (dataReserva, horaReserva, nomeCliente, quantidadePessoas, idMesaReserva))
    return cursor.lastrowid

def verificar_disponibilidade_mesa_db(cursor, idMesaReserva, dataReserva, horaReserva):
    """
    Verifica se a mesa está disponível para reserva na data e hora especificadas.
    Critérios:
    1. A mesa existe em tb_mesas.
    2. A mesa não está marcada como ocupada (statusMesaOcupada = 1).
    3. Não há outra reserva para a mesma mesa na mesma data e hora.
    4. Não há outra reserva dentro do intervalo de 2 horas antes ou depois (apenas reservas não confirmadas).
    """
    # Verifica se a mesa existe e seu status atual
    sql_mesa = "SELECT statusMesaOcupada FROM tb_mesas WHERE idMesa = %s"
    cursor.execute(sql_mesa, (idMesaReserva,))
    mesa_info = cursor.fetchone()

    if not mesa_info:
        return {'disponivel': False, 'motivo': 'Mesa não encontrada.'}

    status_mesa_ocupada = mesa_info[0]
    if status_mesa_ocupada == 1:
        return {'disponivel': False, 'motivo': 'Mesa está atualmente marcada como ocupada.'}

    # Verifica se já existe uma reserva para aquela mesa na data e hora exata
    sql_reserva_existente = "SELECT idReserva FROM tb_reservas WHERE idMesaReserva = %s AND dataReserva = %s AND horaReserva = %s"
    cursor.execute(sql_reserva_existente, (idMesaReserva, dataReserva, horaReserva))
    reserva_existente = cursor.fetchone()

    if reserva_existente:
        return {'disponivel': False, 'motivo': 'Já existe uma reserva para esta mesa, data e hora.'}

    # Verifica se há reservas não confirmadas dentro do intervalo de 2 horas antes ou depois
    dt_reserva = datetime.datetime.combine(dataReserva, horaReserva)
    dt_inicio = (dt_reserva - datetime.timedelta(hours=2))
    dt_fim = (dt_reserva + datetime.timedelta(hours=2))

    sql_intervalo = """
        SELECT idReserva FROM tb_reservas
        WHERE idMesaReserva = %s
        AND dataReserva = %s
        AND statusReservaConfirmada = 0
        AND (
            TIME_TO_SEC(horaReserva) BETWEEN TIME_TO_SEC(%s) AND TIME_TO_SEC(%s)
            OR
            ABS(TIME_TO_SEC(horaReserva) - TIME_TO_SEC(%s)) <= 7200
        )
        """
    cursor.execute(sql_intervalo,
                   (idMesaReserva, dataReserva, dt_inicio.strftime('%H:%M:%S'), dt_fim.strftime('%H:%M:%S'),
                    horaReserva))

    # Reservas encontradas no intervalo de 2 horas
    reservas_intervalo = cursor.fetchall()

    if reservas_intervalo:
        return {'disponivel': False, 'motivo': 'Já existe uma reserva para esta mesa dentro do intervalo de 2 horas.'}

    return {'disponivel': True}

def cancelar_reserva_db(cursor, idReserva):
    """
    Remove uma reserva da tabela tb_reservas pelo id.
    """
    sql = "DELETE FROM tb_reservas WHERE idReserva = %s"
    cursor.execute(sql, (idReserva,))
    return cursor.rowcount

def confirmar_reserva_db(cursor, idReserva):
    """
    Confirma uma reserva alterando o statusReservaConfirmada para 1.
    """
    sql = "UPDATE tb_reservas SET statusReservaConfirmada = 1 WHERE idReserva = %s AND statusReservaConfirmada = 0"
    cursor.execute(sql, (idReserva,))
    return cursor.rowcount

def obter_relatorio_reservas_por_periodo_status_db(cursor, data_inicio, data_fim):
    """
    Retorna o total de reservas agrupadas por data e status no período informado.
    """
    sql = "SELECT dataReserva, statusReservaConfirmada, totalReservas FROM vw_reservas_por_data_e_status WHERE dataReserva BETWEEN %s AND %s"
    cursor.execute(sql, (data_inicio, data_fim))
    return cursor.fetchall()

def obter_reservas_por_mesa_relatorio_db(cursor, idMesa):
    """
    Retorna todas as reservas de uma mesa específica, formatando datas e horários para JSON.
    """
    sql = "SELECT idReserva, dataReserva, horaReserva, idMesaReserva, nomeCliente, quantidadePessoas, statusReservaConfirmada FROM vw_reservas_por_mesa WHERE idMesaReserva = %s"
    cursor.execute(sql, (idMesa,))
    
    colunas = [i[0] for i in cursor.description]
    resultados = []
    for linha in cursor.fetchall():
        registro = {}
        for i, valor in enumerate(linha):
            if isinstance(valor, (datetime.date, datetime.datetime)):
                registro[colunas[i]] = valor.isoformat()
            elif isinstance(valor, datetime.timedelta):
                total_seconds = int(valor.total_seconds())
                hours, remainder = divmod(total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                registro[colunas[i]] = f"{hours:02}:{minutes:02}:{seconds:02}"
            else:
                registro[colunas[i]] = valor
        resultados.append(registro)
        
    return resultados

def obter_mesas_confirmadas_relatorio_db(cursor):
    """
    Retorna o total de confirmações por mesa.
    """
    sql = "SELECT idMesa, totalConfirmacoes FROM vw_confirmacoes_por_mesa"
    cursor.execute(sql)
    return cursor.fetchall()

def executar_query(operacao):
    """
    Decorador para gerenciar conexão e transação com o banco de dados.
    Garante commit, rollback e fechamento de conexão/cursor.
    """
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

# Funções expostas para uso externo, já com gerenciamento de conexão
criar_reserva = executar_query(criar_reserva_db)
verificar_disponibilidade_mesa = executar_query(verificar_disponibilidade_mesa_db)
cancelar_reserva = executar_query(cancelar_reserva_db)
confirmar_reserva = executar_query(confirmar_reserva_db)
obter_relatorio_reservas_periodo_status = executar_query(obter_relatorio_reservas_por_periodo_status_db)
obter_reservas_por_mesa_relatorio = executar_query(obter_reservas_por_mesa_relatorio_db)
obter_mesas_confirmadas_relatorio = executar_query(obter_mesas_confirmadas_relatorio_db)