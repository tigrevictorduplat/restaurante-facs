import mysql.connector

def conectar_banco(operacao, *args, **kwargs):
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='banco_restaurante',
    )
    cursor = conexao.cursor()

    try:
        resultado = operacao(cursor, *args, **kwargs)  # Executa a função com os argumentos
        conexao.commit()
        return resultado
    except Exception as e:
        conexao.rollback()
        print("Erro ao executar operação:", e)
    finally:
        cursor.close()
        conexao.close()
