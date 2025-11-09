import tkinter as tk
from PIL import Image, ImageTk
from requests import session
from yaml import compose_all
import ventanas
from control_db import GestorUsuarios, GestorCliente, GestorAparatos, GestorRegistros

# Crear todas las tablas necesarias
GestorUsuarios.crear_tabla()
GestorCliente.crear_tabla()
GestorAparatos.crear_tabla()
GestorRegistros.crear_tabla()

from ventanas import Login

if __name__ == "__main__":
    app = Login()
    app.run()

