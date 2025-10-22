import sqlite3

DB_NAME = "Taller.db"


class Taller:
    def __init__(self):
        self.nombre = "Taller de Reparación"

    @staticmethod
    def _conn():
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory =sqlite3.Row
        return conn

    def crear_tablas(self):
        conn = self._conn()
        cursor = conn.cursor()

        cursor.execute("""  
        CREATE TABLE IF NOT EXISTS usuarios(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            usuario TEXT,
            contra TEXT
        )    
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cliente(
            nit INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            celular TEXT,
            direccion TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS aparatos(
            no INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT,
            marca TEXT,
            modelo TEXT,
            falla TEXT,
            cliente_nit TEXT
            FOREIGN KEY(cliente_nit) REFERENCES cliente(nit)
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS bodega(
            pieza INTEGER PRIMARY KEY AUTOINCREMENT,
            producto TEXT,
            modelo TEXT
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS registros_entradas(
            registro INTEGER PRIMARY KEY AUTOINCREMENT,
            no_aparato INTEGER,
            id_trabajador INTEGER,
            cliente_nit INTEGER
            presupuesto REAL,
            FOREIGN KEY(no_aparato) REFERENCES aparatos(no)
            FOREIGN KEY(id_trabajador) REFERENCES usuarios(id)
            FOREIGN KEY(cliente_nit) REFERENCES cliente(nit)
        )
        """)


