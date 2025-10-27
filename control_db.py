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
        CREATE TABLE IF NOT EXISTS clientes(
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
            registro_entrada INTEGER PRIMARY KEY AUTOINCREMENT,
            no_aparato INTEGER,
            id_trabajador INTEGER,
            cliente_nit INTEGER
            presupuesto REAL,
            FOREIGN KEY(no_aparato) REFERENCES aparatos(no)
            FOREIGN KEY(id_trabajador) REFERENCES usuarios(id)
            FOREIGN KEY(cliente_nit) REFERENCES cliente(nit)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS registros_salidas(
            registro_salida INTEGER PRIMARY KEY AUTOINCREMENT,
            no_aparato INTEGER,
            no_registro_entrada INTEGER,
            id_trabajador INTEGER,
            total REAL,
            FOREIGN KEY(no_aparato) REFERENCES aparatos(no)
            FOREIGN KEY(no_registro) REFERENCES registros_entradas(registro_entrada) 
        )   
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimiento_bodega(
            registro_bodega INTEGER PRIMARY KEY AUTOINCREMENT,
            id_trabajador INTEGER,
            fecha TEXT,
            aparato TEXT,
            modelo TEXT,
            FOREIGN KEY(id_trabajador) REFERENCES usuarios(id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS detalle_trabajos(
            no_registro_entrada INTEGER 
            no_registros_salida INTEGER 
            total_cobrado INTEGER
            FOREIGN KEY(no_registro_entrada) REFERENCES registros_entradas
            FOREIGN KEY(no_registro_salida) REFERENCES registros_salidas
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS detalle_historial(
            no_registro INTEGER,
            nit_cliente INTEGER,
            total INTEGER,
            FOREIGN KEY(total) REFERENCES detalle_trabajos(total_cobrado)
        )
        """)




