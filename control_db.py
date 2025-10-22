import sqlite3

DB_NAME = "Taller.db"


class Taller:
    def __init__(self):
        self.nombre = "Taller de Reparación"

    @staticmethod
    def _conn():
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory =sqlite3.Row

    def crear_tablas(self):
        conn = self._conn()
        cursor = conn.cursor()

        cursor.excute("""  
        CREATE TABLE IF NOT EXISTS usuarios(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            usuario TEXT,
            contra TEXT
        )    
        """)

        cursor.excute("""
        CREATE TABLE IF NOT EXISTS aparatos(
            no INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT,
            marca TEXT,
            modelo TEXT,
            falla TEXT,
            cliente TEXT
        )
        """)

        cursor.excute("""
        CREATE TABLE IF NOT EXISTS cliente(
            nit INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            celular TEXT,
            direccion TEXT
        )
        """)

