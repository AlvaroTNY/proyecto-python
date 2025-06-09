# database.py
import mysql.connector
from mysql.connector import Error

def crear_conexion():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='gestor_escolar'
        )
        if conexion.is_connected():
            return conexion
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
    return None

# No es necesario inicializar tablas aquí, ya que se crean en phpMyAdmin.