import sqlite3

from jaraco.functools import result_invoke
from orca.braille import cursorCell


class BaseDB:
    DB_NAME = "Taller.db" #Se crea la base de datos con el nombre asignado

    @staticmethod
    def _conn():
        conn = sqlite3.connect(BaseDB.DB_NAME) #Se conecta con la base de datos
        conn.row_factory = sqlite3.Row
        return conn


class Usuario: #Clase para instancias usuarios
    def __init__(self, nombre, usuario, contra, rol):
        self.nombre = nombre
        self.usuario = usuario
        self.contra = contra
        self.rol = rol
    def __repr__(self):
        return f"Usuario(nombre='{self.nombre}', usuario='{self.usuario}', rol='{self.rol}')"


class GestorUsuarios(BaseDB):
    @staticmethod  # Este metodo sirve para crear la tabla sobre los usuarios
    def crear_tabla():
        conn = BaseDB._conn()
        cursor = conn.cursor()
        cursor.execute("""
              CREATE TABLE IF NOT EXISTS usuarios(
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  nombre TEXT NOT NULL,
                  usuario TEXT UNIQUE NOT NULL,
                  contra TEXT NOT NULL,
                  rol TEXT NOT NULL CHECK(rol IN ('admin', 'trabajador', 'dev')) 
              )
          """)
        conn.commit()
        conn.close()

    @staticmethod  # Este metodo se llama para cuando se desean ingresar usuarios y que se guarden
    def insertar_usuario(usuario: Usuario):
        conn = BaseDB._conn()
        cursor = conn.cursor()
        cursor.execute("""
              INSERT INTO usuarios(nombre, usuario, contra, rol)
              VALUES (?,?,?,?)
          """, (usuario.nombre, usuario.usuario, usuario.contra, usuario.rol))
        conn.commit()
        conn.close()
    @staticmethod
    def validar_credenciales(usuario, contra):
        conn = BaseDB._conn()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM usuarios WHERE usuario = ? AND contra = ?
        """, (usuario, contra))
        resultados = cursor.fetchone()
        conn.close()
        return resultados

    @staticmethod
    def listar_todos():
        conn = BaseDB._conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ususarios")
        resultados = cursor.fetchall()
        conn.close()
        return resultados

    @staticmethod
    def actualizar_usuario(id_usuario, nuevo_nombre, nuevo_usuario, nueva_contra, nuevo_rol):
        conn = BaseDB._conn()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE usuarios
            SET nombre =?, usuarios =?, contra=?, rol=?
            WHERE id=?
        """, (nuevo_nombre, nuevo_usuario, nueva_contra, nuevo_rol, id_usuario))
        conn.commit()
        conn.close()

    @staticmethod
    def borrar_usuario(id_usuario):
        conn = BaseDB._conn()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id=?", (id_usuario,))
        conn.commit()
        conn.close()


class Cliente:

    def __init__(self, nit, nombre, celular, direccion):
        self.nit = nit
        self.nombre = nombre
        self.celular = celular
        self.direccion = direccion

    def __repr__(self):
        return f"Cliente(nit='{self.nit}', nombre='{self.nombre}')"

class GestorCliente(BaseDB):
    @staticmethod
    def crear_tabla(): #Funcion para crear la tabla de los clientes
        conn = BaseDB._conn()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes(
                nit TEXT UNIQUE PRIMARY KEY,
                nombre TEXT NOT NULL,
                celular TEXT UNIQUE NOT NULL,
                direccion TEXT NOT NULL
            )
         """)
        conn.commit()
        conn.close()

    @staticmethod #Funcion para insertar nuevos clientes
    def insertar_cliente(cliente : Cliente):
        conn = BaseDB._conn()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO clientes (nit, nombre, celular, direccion)
            VALUES(?,?,?,?)
        """,(cliente.nit, cliente.nombre, cliente.celular, cliente.direccion))
        conn.commit()
        conn.close()

    @staticmethod #Funcion para listar todos los clientes
    def listar_clientes():
        conn = BaseDB._conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes")
        resultados = cursor.fetchall()
        conn.close()
        return resultados

    @staticmethod
    def buscar_por_nit(nit):
        conn = BaseDB._conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes WHERE nit = ?", (nit,))
        resultado = cursor.fetchone()
        conn.close()
        return resultado

    @staticmethod
    def existe_cliente(nit):
        return GestorCliente.buscar_por_nit(nit) is not None

    @staticmethod
    def actualizar_cliente(nit, nuevo_nombre, nuevo_celular, nueva_direccion):
        conn = BaseDB._conn()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE clientes
            SET nombre = ?, celular = ?, direccion = ?
            WHERE nit=?
        """, (nuevo_nombre, nuevo_celular, nueva_direccion, nit))
        conn.commit()
        conn.close()

    @staticmethod
    def borrar_cliente(nit):
        conn = BaseDB._conn()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clientes WHERE nit = ?", (nit,))
        conn.commit()
        conn.close()


class Aparatos:
    def __init__(self, marca, modelo, aparato, falla):
        self.marca = marca
        self.modelo = modelo
        self.aparato = aparato
        self.falla = falla


class GestorAparatos(BaseDB):
    @staticmethod
    def crear_tabla():
        conn = BaseDB._conn()
        cursor = conn.cursor()
        cursor.execute("""
               CREATE TABLE IF NOT EXISTS aparatos(
                no_aparato INTEGER PRIMARY KEY AUTOINCREMENT,
                marca TEXT NOT NULL,
                modelo TEXT NOT NULL,
                tipo TEXT NOT NULL,
                falla TEXT NOT NULL,
                cliente_nit TEXT NOT NULL,
                FOREIGN KEY(cliente_nit) REFERENCES clientes(nit) ON DELETE CASCADE
                )
        """)

    @staticmethod
    def insertar_aparato(aparato: Aparatos, cliente_nit: str):
        conn = BaseDB._conn()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO aparatos(marca, modelo, tipo, falla, cliente_nit)
            VALUES (?,?,?,?,?)
        """, (aparato.marca, aparato.modelo, aparato.aparato, aparato.falla, cliente_nit ))
        conn.commit()
        conn.close()

    @staticmethod
    def listar_aparatos():
        conn = BaseDB._conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM aparatos")
        resultados = cursor.fetchall()
        conn.close()
        return resultados

    @staticmethod
    def borrar_aparato(no_aparato):
        conn = BaseDB._conn()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM aparatos WHERE no_aparato=?", (no_aparato,))
        conn.commit()
        conn.close()

#Esta clase se encarga de registrar las entradas y salidas de los aparatos
class Registro:
    def __init__(self, fecha, cliente_nit, no_aparato, estado, id_trabajador):
        self.fecha = fecha
        self.cliente_nit = cliente_nit
        self.no_aparato = no_aparato
        self.estado = estado
        self.id_trabajador = id_trabajador

class GestorRegistros(BaseDB):

    @staticmethod
    def crear_tabla():
        conn = BaseDB._conn()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS registros(
            no_registro INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            cliente_nit TEXT NOT NULL,
            no_aparato INTEGER NOT NULL,
            id_trabajador INTEGER NOT NULL,
            FOREIGN KEY(cliente_nit) REFERENCES clientes(nit)
            FOREIGN KEY(no_aparato) REFERENCES aparatos(no_aparato)
            FOREIGN KEY(id_trabajador) REFERENCES usuarios(id)
            )
        """)
        conn.commit()
        conn.close()
    @staticmethod
    def insertar_registro(registro : Registro):
        conn = BaseDB._conn()
        cursor = conn.cursor()
        cursor.execute("""  
            INSERT INTO registros(fecha, estado, cliente_nit, no_aparato, id_trabajador)
            VALUES (?, ?, ?, ?, ?)
        """, (registro.fecha, registro.estado, registro.cliente_nit, registro.no_aparato, registro.id_trabajador))
        conn.commit()
        conn.close()

    @staticmethod
    def listar_registros():
        conn = BaseDB._conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM registros")
        resultados = cursor.fetchall()
        conn.close()
        return resultados

    @staticmethod
    def filtrar_estado(estado):
        conn = BaseDB._conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM registros WHERE estado =?", (estado,))
        resultados = cursor.fetchall()
        conn.close()
        return resultados

















