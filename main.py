import tkinter as tk
from PIL import Image, ImageTk
import ventanas
from control_db import GestorUsuarios, GestorCliente, GestorAparatos, GestorRegistros

# Crear todas las tablas necesarias
def inicializar_bd():
    GestorUsuarios.crear_tabla()
    GestorCliente.crear_tabla()
    GestorAparatos.crear_tabla()
    GestorRegistros.crear_tabla()
from ventanas import Login

if __name__ == "__main__":
    inicializar_bd()
    app = Login()
    app.run()

