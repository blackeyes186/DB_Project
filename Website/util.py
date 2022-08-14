import pymysql.cursors
from flask import flash

def query_insert(sql, connection):
    result = 1
    try:
        with connection.cursor() as cursor:
            # Insert a new record
            cursor.execute(sql)
        connection.commit()
    except:
        result = 0
    return result

def query_fetchone(sql, connection):
    with connection.cursor() as cursor:
        # Read a single record
        cursor.execute(sql)
        result = cursor.fetchone()
    connection.commit()
    return result


def query_fetchall(sql, connection):
    with connection.cursor() as cursor:
        # Read all records
        cursor.execute(sql)
        result = cursor.fetchall()
    connection.commit()
    return result