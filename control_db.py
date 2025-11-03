import sqlite3


class BaseDB:
    DB_NAME = "Taller.db" #Se crea la base de datos con el nombre asignado

    @staticmethod
    def _conn():
        conn = sqlite3.connect(BaseDB.DB_NAME) #Se conecta con la base de datos
        conn.row_factory = sqlite3.Row
        return conn

class Administrador(BaseDB):
    @staticmethod
    def crear_tabla():
        conn = BaseDB._conn()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS administrador (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                usuario TEXT UNIQUE NOT NULL,
                contra TEXT NOT NULL
            )
            """)
        conn.commit()
        conn.close()

class Usuario(BaseDB):
    @staticmethod
    def crear_tabla():
        conn = BaseDB._conn()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuario(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                usuario TEXT UNIQUE NOT NULL,
                contra TEXT NOT NULL
            )
            """)
class Cliente(BaseDB):
    @staticmethod
    def crear_tabla():
        conn = BaseDB._conn()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cliente(
                nit INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                celular TEXT NOT NULL,
                direccion TEXT NOT NULL
            )
            """)

class











