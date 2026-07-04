import os
import psycopg2

def conectar():
    try:
        conexion = psycopg2.connect(os.environ.get("DATABASE_URL"))
        return conexion
    except Exception as e:
        print("Error al conectar:", e)
        return None

def desconectar(conexion):
    if conexion:
        conexion.close()