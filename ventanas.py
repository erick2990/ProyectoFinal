import sqlite3
import tkinter as tk
from PIL import Image, ImageTk
from datetime import date
from tkinter import messagebox, ttk
import calendar
from control_db import Usuario, GestorUsuarios
from netaddr.strategy.ipv6 import width
from oauthlib.uri_validate import hier_part
from pygments import highlight
fecha = date.today()

admin_maestro = Usuario("Administrador", "Erick", "1234", "dev")
GestorUsuarios.insertar_usuario(admin_maestro)
try:
    GestorUsuarios.insertar_usuario(admin_maestro)
except Exception as e:
    print('Error')

def aplicar_logo(canvas, ruta_logo):
    logo = Image.open(ruta_logo).convert("RGBA")
    logo = logo.resize((800, 600))
    logo_tk = ImageTk.PhotoImage(logo)
    canvas.create_image(0, 0, anchor="nw", image=logo_tk)
    canvas.logo_img = logo_tk

class Login:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TALLER ELECTRÓNICO")
        self.root.geometry("800x600") #Se creo la ventana root
        canvas = tk.Canvas(self.root, width=800, height=600, highlightthickness=0) #Se añade un canva a la ventana root
        canvas.pack(fill="both", expand=True) #Se coloca
        fondo = Image.open("/home/erick/Documentos/ProyectoFinal/util/fondo.png") #abrir fondo
        fondo = fondo.resize((800, 600))
        fondo_tk = ImageTk.PhotoImage(fondo)
        canvas.create_image(0, 0, anchor="nw", image=fondo_tk)
        canvas.fondo_img = fondo_tk #colocar fondo
        logotipo = Image.open("/home/erick/Documentos/ProyectoFinal/util/Logotipo.png").convert("RGBA") #abrir logo
        logotipo = logotipo.resize((350, 350))
        logo_tk = ImageTk.PhotoImage(logotipo)
        canvas.create_image(250, 250, anchor="center", image=logo_tk)
        canvas.logo_img = logo_tk #colocar logo
        #Texto
        canvas.create_text(600, 150, text="Inicio de sesión", font=("Arial", 14, "bold"), fill="white")
        canvas.create_text(530, 200, text="Usuario: ", font=("Arial", 14, "italic"), fill="white")
        canvas.create_text(550, 300, text="Contraseña: ", font=("Arial", 14, "italic"), fill="white")
        #Datos
        self.ingreso_usuario = tk.Entry(canvas, font=("Arial", 12), bg="white", fg="black", width=20)
        canvas.create_window(585, 250, window=self.ingreso_usuario)
        self.ingreso_contra = tk.Entry(canvas, font=("Arial", 12), bg="white", show="*", width=20)
        canvas.create_window(585, 350, window=self.ingreso_contra)
        #Proceso para revelar la contraseña o ocultarla
        self.mostrar_contra = tk.BooleanVar()  # Esta variable sirve para saber si el usuario decide ver la contraseña o no
        def revelar_contra():
            if self.mostrar_contra.get():
                self.ingreso_contra.config(show="") #com esto se muestra el texto
            else:
                self.ingreso_contra.config(show="*") #oculta la contraseña
        checkbox = tk.Checkbutton(canvas, text="Ver contraseña", variable=self.mostrar_contra, command=revelar_contra,font=("Arial", 10, "italic"), bg="white")
        canvas.create_window(550, 400, window=checkbox)
        self.sesion_valida = tk.BooleanVar() #Guarda la variable si eñ usuario ingreso credenciales correctas
        boton_iniciar = tk.Button(canvas, text="Iniciar Sesión", font=("Arial", 12, "bold"), command=self.validar, bg="RoyalBlue4", fg="white")
        canvas.create_window(600, 450, window=boton_iniciar)

    def validar(self):
        usuario = self.ingreso_usuario.get()
        contra = self.ingreso_contra.get()
        #if usuario == "admin" and contra == "1234":
        #    self.root.withdraw()
        #    Maestra(self.root, self)
        if not usuario or not contra:
            messagebox.showwarning("Campos vacíos", "Por favor, completa todos los campos antes de continuar.")
            return

        resultado = GestorUsuarios.validar_credenciales(usuario, contra)

        if resultado:
            rol = resultado["rol"]
            self.root.withdraw()
            if rol == "admin":
                SubAdmin(self.root, self)
            elif rol == "dev":
                Maestra(self.root, self)
            elif rol == "trabajador":
                SubTrabajador(self.root, self)
            else:
                messagebox.showinfo("Acceso", f"Rol no reconocido: {rol}")
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")
            self.ingreso_usuario.delete(0, tk.END)
            self.ingreso_contra.delete(0, tk.END)


    def run(self):
        self.root.mainloop()

class Maestra:
    def __init__(self, master, login_ref):
        self.login_ref = login_ref
        self.ventana_maestra = tk.Toplevel(master)
        self.ventana_maestra.title("VENTANA MAESTRA")
        self.ventana_maestra.geometry("800x600")
        self.canvas = tk.Canvas(self.ventana_maestra, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)
        aplicar_logo(self.canvas, "/home/erick/Documentos/ProyectoFinal/util/fondo.png")
        self.contenido = tk.Frame(self.ventana_maestra, width=800, height=600)
        self.contenido.pack_forget()  # ocultar al inicio

        self.canvas.create_text(100, 50, text="NOMBRE:", font=("Arial", 14, "bold"), fill="white")
        self.canvas.create_text(500, 50, text="USUARIO:", font=("Arial", 14, "bold"), fill="white")
        self.canvas.create_text(125, 200, text="CONTRASEÑA:", font=("Arial", 14, "bold"), fill="white")
        self.canvas.create_text(500, 200, text="REPETIR CONTRASEÑA:", font=("Arial", 14, "bold"), fill="white")
        self.canvas.create_text(200, 400, text="(ROL POR DEFECTO ADMINSTRADOR)", font=("Arial", 12, "italic"), fill="white")
        self.entry_nombre = tk.Entry(self.ventana_maestra, font=("Arial", 12))
        self.canvas.create_window(125, 100, window=self.entry_nombre)

        self.entry_usuario = tk.Entry(self.ventana_maestra, font=("Arial", 12))
        self.canvas.create_window(500, 100, window=self.entry_usuario)

        self.entry_contra = tk.Entry(self.ventana_maestra, show="*", font=("Arial", 12))
        self.canvas.create_window(125, 250, window=self.entry_contra)

        self.entry_repetir = tk.Entry(self.ventana_maestra, show="*", font=("Arial", 12))
        self.canvas.create_window(500, 250, window=self.entry_repetir)

        agregar_admin = tk.Button(self.ventana_maestra, text="CREAR ADMINISTRADOR", font=("Arial", 14, "bold"), command=self.crear_admin,highlightthickness=3, highlightbackground="dark slate gray", bg="gray20", fg="white")
        self.canvas.create_window(650, 550, window=agregar_admin)

        cerrar_B = tk.Button(self.ventana_maestra, text="CANCELAR", font=("Arial", 14, "bold"), command=self.cerrar_sesion, highlightthickness="3", highlightbackground="dark slate gray",bg="gray20", fg="white")
        self.canvas.create_window(450, 550, window=cerrar_B)

        self.mostrar_contra = tk.BooleanVar()  # Esta variable sirve para saber si el usuario decide ver la contraseña o no

        def revelar_contra():
            if self.mostrar_contra.get():
                self.entry_contra.config(show="")  # com esto se muestra el texto
                self.entry_repetir.config(show="")
            else:
                self.entry_contra.config(show="*")  # oculta la contraseña
                self.entry_repetir.config(show="*")

        checkbox = tk.Checkbutton(self.canvas, text="MOSTRAR CONTRASEÑAS", variable=self.mostrar_contra, command=revelar_contra,font=("Arial", 10, "italic"), bg="white")
        self.canvas.create_window(125, 275, window=checkbox)

    def cerrar_sesion(self):
        self.ventana_maestra.destroy()
        self.ventana_maestra.master.deiconify()
        if hasattr(self.login_ref, "ingreso_usuario") and hasattr(self.login_ref, "ingreso_contra"):
            self.login_ref.ingreso_usuario.delete(0, tk.END)
            self.login_ref.ingreso_contra.delete(0, tk.END)



    def crear_admin(self):
        nombre = self.entry_nombre.get()
        usuario = self.entry_usuario.get()
        contra = self.entry_contra.get()
        repetir = self.entry_repetir.get()

        if not all([nombre, usuario, contra, repetir]):
            messagebox.showwarning("Campos vacíos", "Por favor completa todos los campos.")
            return

        if contra != repetir:
            messagebox.showerror("Error", "Las contraseñas no coinciden.")
            return

        nuevo = Usuario(nombre, usuario, contra, "admin")
        try:
            GestorUsuarios.insertar(nuevo)
            messagebox.showinfo("Éxito", "Administrador creado correctamente.")
            self.cerrar_sesion()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El usuario ya existe.")


class SubTrabajador:

    def __init__(self, master, login_ref):
        self.login_ref = login_ref
        self.sub = tk.Toplevel(master)
        self.sub.title("TRABAJADOR")
        self.sub.geometry("800x600")
        self.canvas  = tk.Canvas(self.sub, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)
        aplicar_logo(self.canvas, "/home/erick/Documentos/ProyectoFinal/util/fondo.png")
        self.contenido = tk.Frame(self.sub, width=800, height=600)
        self.contenido.pack_forget() #ocultar al inicio

        self.frames = {}
        self.crear_frames()
        registrar_aparatoB = tk.Button(self.sub, text="REGISTRAR\nAPARATO", font=("Arial", 14, "bold"), command=self.mostrar_aparato, highlightthickness=3, highlightbackground="dark slate gray", bg="gray20", fg="white")
        self.canvas.create_window(100, 200, window = registrar_aparatoB)
        cotizar_B = tk.Button(self.sub, text="COTIZACIÓN DE\nREPARACIÓN", font=("Arial", 14, "bold"), command=self.mostrar_cotizacion,highlightthickness=3, highlightbackground="dark slate gray", bg="gray20", fg="white")
        self.canvas.create_window(400, 200 , window=cotizar_B)
        consulta_B = tk.Button(self.sub, text="CONSULTA DE\nREPARACIONES", font=("Arial", 14, "bold"),command=self.mostrar_historial,highlightthickness=3, highlightbackground="dark slate gray", bg="gray20", fg="white")
        self.canvas.create_window(685,200, window=consulta_B)
        bodega_B = tk.Button(self.sub, text="BODEGA", font=("Arial", 14, "bold"), command=self.mostrar_bodega, highlightthickness=3, highlightbackground="dark slate gray", width=15, height=2, bg="gray20", fg="white")
        self.canvas.create_window(400, 300, window=bodega_B)
        cerrar_B = tk.Button(self.sub, text="CERRAR SESIÓN", font=("Arial", 14, "bold"),command=self.cerrar_sesion, highlightthickness="3", highlightbackground="dark slate gray", width=15, height=2, bg="gray20", fg="white")
        self.canvas.create_window(400, 500, window=cerrar_B)

    def crear_frames(self):
        # Aquí defines los frames como si fueran pantallas
        self.frames["aparato"] = AgregarAparato(self.contenido, self)
        self.frames["cotizacion"] = Cotizacion(self.contenido, self)
        self.frames["historial"] = BuscarHistorial(self.contenido, self)
        self.frames["bodega"] = Bodega(self.contenido, self)

    def mostrar_frame(self, nombre):
        self.canvas.pack_forget() #oculta el canvas
        self.contenido.pack(fill="both", expand=True)
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[nombre].pack(fill="both", expand=True)

    def volver_menu(self):
        self.contenido.pack_forget()
        for frame in self.frames.values():
            frame.pack_forget()
        self.canvas.pack(fill="both", expand=True) #vuelve a mostrar el submenu Cambio para que reaparezca

    def mostrar_aparato(self):
        self.mostrar_frame("aparato")

    def mostrar_cotizacion(self):
        self.mostrar_frame("cotizacion")

    def mostrar_historial(self):
        self.mostrar_frame("historial")

    def mostrar_bodega(self):
        self.mostrar_frame("bodega")

    def cerrar_sesion(self):
        self.sub.destroy()
        self.sub.master.deiconify()
        if hasattr(self.login_ref, "ingreso_usuario") and hasattr(self.login_ref, "ingreso_contra"):
            self.login_ref.ingreso_usuario.delete(0, tk.END)
            self.login_ref.ingreso_contra.delete(0, tk.END)

class SubAdmin:
    def __init__(self, master, login_ref):
        self.login_ref = login_ref
        self.sub = tk.Toplevel(master)
        self.sub.title("Administrador")
        self.sub.geometry("800x600")
        self.canvas = tk.Canvas(self.sub, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)
        aplicar_logo(self.canvas, "/home/erick/Documentos/ProyectoFinal/util/fondo.png")
        self.contenido = tk.Frame(self.sub, width=800, height=600)
        self.contenido.pack_forget()

        self.frames = {} #Se crea un diccionario de frames para ser invocados
        self.crear_frame() #Se llama a la funcion de crear frames

        trabajadores_B = tk.Button(self.sub, text="TRABAJADORES", font=("Arial",14, "bold"), command=self.mostrar_trabajador , highlightthickness=3, highlightbackground="dark slate gray", width=15, height=2, bg="gray20", fg="white")
        self.canvas.create_window(100, 200, window=trabajadores_B)
        estadisticas_B = tk.Button(self.sub, text="ESTADISTICAS", font=("Arial", 14, "bold"), highlightthickness=3, highlightbackground="dark slate gray", width=15, height=2, bg="gray20", fg="white")
        self.canvas.create_window(400, 200, window=estadisticas_B)
        consulta_B = tk.Button(self.sub, text="CONSULTA DE\nREPARACIONES" ,font=("Arial", 14, "bold"), command=self.mostrar_historial, highlightthickness=3, highlightbackground="dark slate gray", width=15, height=2, bg="gray20", fg="white")
        self.canvas.create_window(700, 200, window=consulta_B)
        bodega_B = tk.Button(self.sub, text="BODEGA", font=("Arial", 14, "bold"), command=self.mostrar_bodega, highlightthickness=3, highlightbackground="dark slate gray", width=15, height=2, bg="gray20", fg="white")
        self.canvas.create_window(100, 300, window=bodega_B)
        clientes_B = tk.Button(self.sub, text="CLIENTES", font=("Arial", 14, "bold"), command=self.mostrar_clientes, highlightthickness=3, highlightbackground="dark slate gray", width=15, height=2, bg="gray20", fg="white")
        self.canvas.create_window(400, 300, window=clientes_B)
        cobros_B = tk.Button(self.sub, text="HISTORIAL\nCOBROS", font=("Arial", 14, "bold"), command=self.mostrar_cobros, highlightthickness=3, highlightbackground="dark slate gray", width=15, height=2, bg="gray20", fg="white")
        self.canvas.create_window(700, 300, window=cobros_B)
        cerrar_B = tk.Button(self.sub, text="CERRAR SESIÓN", font=("Arial",14,"bold"), command=self.cerrar_sesion, highlightthickness=3, highlightbackground="dark slate gray", width=15, height=2, bg="gray20", fg="white")
        self.canvas.create_window(400, 500, window=cerrar_B)

    def crear_frame(self):
        self.frames["trabajador"] = Trabajador(self.contenido, self)
        #self.frames["estadisticas"] = aqui el codigo para estadistica
        self.frames["historial"] = BuscarHistorial(self.contenido, self)
        self.frames["bodega"] = Bodega(self.contenido, self)
        self.frames["clientes"] = Clientes(self.contenido, self)
        self.frames["cobros"] = Cobros(self.contenido, self)

    def mostrar_frame(self, nombre):
        self.canvas.pack_forget()
        self.contenido.pack(fill="both", expand=True)
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[nombre].pack(fill="both", expand=True)

    def mostrar_trabajador(self):
        self.mostrar_frame("trabajador")
    def mostrar_estadistica(self):
        self.mostrar_frame("estadisticas")
    def mostrar_historial(self):
        self.mostrar_frame("historial")
    def mostrar_bodega(self):
        self.mostrar_frame("bodega")
    def mostrar_clientes(self):
        self.mostrar_frame("clientes")
    def mostrar_cobros(self):
        self.mostrar_frame("cobros")

    def volver_menu(self):
        self.contenido.pack_forget()
        for frame in self.frames.values():
            frame.pack_forget()
        self.canvas.pack(fill="both", expand=True) #vuelve a mostrar el submenu

    def cerrar_sesion(self):
        self.sub.destroy()
        self.sub.master.deiconify()
        if hasattr(self.login_ref, "ingreso_usuario") and hasattr(self.login_ref, "ingreso_contra"):
            self.login_ref.ingreso_usuario.delete(0, tk.END)
            self.login_ref.ingreso_contra.delete(0, tk.END)

class AgregarAparato(tk.Frame):
    def __init__(self, master, ref_sub):
        super().__init__(master, width=800, height=600)
        self.ref_sub = ref_sub
        self.pack_propagate(False)
        canvas = tk.Canvas(self, width=800, height=600)
        canvas.pack(fill="both", expand=True)
        aplicar_logo(canvas, "/home/erick/Documentos/ProyectoFinal/util/fondo.png")
        titulo = tk.Label(self, text="AGREGAR APARATO", font=("Arial",14,"italic"), width=20, height=2)
        canvas.create_window(350, 50, window=titulo)
        dato_etiqueta = tk.Label(self, text="DATOS CLIENTE: ", font=("Arial", 14, "bold"), width=20, height=2)
        canvas.create_window(100, 100, window=dato_etiqueta)
        detalles_etiqueta = tk.Label(self, text=" DETALLES APARATO: ", font=("Arial", 14, "bold"), width=20, height=2)
        canvas.create_window(100,350, window=detalles_etiqueta)
        fecha_etiqueta = tk.Label(self, text=f"{fecha.strftime("%d/%m/%y")}", font=("Arial", 12, "bold"), bg="white",width=10, height=2)
        canvas.create_window(620, 50, window=fecha_etiqueta)
        caso_etiqueta = tk.Label(self, text="No. 0000", font=("Arial", 12, "bold"), bg="white", width=10, height=2)
        canvas.create_window(700, 50, window=caso_etiqueta)
        canvas.create_text(50, 150, text="NIT:", font=("Arial", 14, "italic"), fill="white")
        canvas.create_text(200, 150, text="NOMBRE: ", font=("Arial", 14, "italic"), fill="white")
        canvas.create_text(600, 150, text="CELULAR: ", font=("Arial", 14, "italic"), fill="white")
        canvas.create_text(90, 250, text="DIRECCIÓN: ", font=("Arial", 14, "italic"), fill="white")
        canvas.create_text(80, 400, text="MARCA: ", font=("Arial", 14, "italic"), fill="white")
        canvas.create_text(250, 400, text="MODELO: ", font=("Arial", 14, "italic"), fill="white")
        canvas.create_text(600, 400, text="TIPO DE APARATO: ", font=("Arial", 14, "italic"), fill="white")
        canvas.create_text(80, 500, text="FALLA: ", font=("Arial", 14, "italic"), fill="white")
        canvas.create_text(400, 500, text="SUBTOTAL: ", font=("Arial", 14, "bold"), fill="white")
        nit = tk.Entry(self, font=("Arial", 12), bg="white",fg="black" ,width=12)
        canvas.create_window(60, 175, window=nit)
        nombre = tk.Entry(self, font=("Arial", 12), bg="white", fg="black", width=40)
        canvas.create_window(340, 175, window=nombre)
        celular = tk.Entry(self, font=("Arial", 12), bg="white", fg="black", width=20)
        canvas.create_window(630, 175, window=celular)
        direccion = tk.Entry(self, font=("Arial", 12), bg="white", fg="black", width=30)
        canvas.create_window(140, 300, window=direccion)
        marca = tk.Entry(self, font=("Arial", 12), bg="white", fg="black", width=20)
        canvas.create_window(100, 450, window=marca)
        modelo = tk.Entry(self, font=("Arial", 12), bg="white", fg="black", width=15)
        canvas.create_window(280, 450, window=modelo)
        falla = tk.Entry(self, font=("Arial", 12), bg="white", fg="black", width=15)
        canvas.create_window(100, 550, window=falla)
        aparatos_validos = ["Televisor", "Radio", "Teatro en casa", "Herramienta", "Baterías"]
        tipo_aparato = tk.StringVar() #Aqui se guardara que tipo de aparato selecciono el usuario
        listado_aparatos = tk.OptionMenu(self, tipo_aparato, *aparatos_validos)
        canvas.create_window(600, 450, window=listado_aparatos)
        subTotal = tk.Label(self, text="Q.0", font=("Arial",12, "bold"), width=15, highlightthickness=3, highlightbackground="black")
        canvas.create_window(400, 550, window=subTotal)
        cancelar_B = tk.Button(self, text="CANCELAR",font=("Arial", 12, "bold"), command=self.ref_sub.volver_menu, bg="gray20", fg="white")
        canvas.create_window(600, 575, window=cancelar_B)
        aceptar_B = tk.Button(self, text="ACEPTAR", font=("Arial", 12, "bold"),command=self.aceptar ,bg="gray20", fg="white")
        canvas.create_window(725, 575, window=aceptar_B)

    def aceptar(self):
        #Aqui el codigo que se ejecuta para guardar los datos
        pass

class Cotizacion(tk.Frame):
    def __init__(self, master, ref_sub):
        super().__init__(master, width=800, height=600)
        self.ref_sub = ref_sub
        self.pack_propagate(False)
        canvas = tk.Canvas(self, width=800, height=600)
        canvas.pack(fill="both", expand=True)
        aplicar_logo(canvas, "/home/erick/Documentos/ProyectoFinal/util/fondo.png")
        titulo = tk.Label(self, text="COTIZACIÓN DE APARATO", font=("Arial", 14, "italic"), width=24, height=2)
        canvas.create_window(350, 50, window=titulo)
        dato_etiqueta = tk.Label(self, text="DATOS CLIENTE: ", font=("Arial", 14, "bold"), width=20, height=2)
        canvas.create_window(100, 100, window=dato_etiqueta)
        detalles_etiqueta = tk.Label(self, text=" DETALLES APARATO: ", font=("Arial", 14, "bold"), width=20, height=2)
        canvas.create_window(100,350, window=detalles_etiqueta)
        fecha_etiqueta = tk.Label(self, text=f"{fecha.strftime("%d/%m/%y")}", font=("Arial", 12, "bold"), bg="white",width=10, height=2)
        canvas.create_window(620, 50, window=fecha_etiqueta)
        caso_etiqueta = tk.Label(self, text="No. 0000", font=("Arial", 12, "bold"), bg="white", width=10, height=2)
        canvas.create_window(700, 50, window=caso_etiqueta)
        canvas.create_text(50, 150, text="NIT:", font=("Arial", 14, "italic"), fill="white")
        canvas.create_text(200, 150, text="NOMBRE: ", font=("Arial", 14, "italic"), fill="white")
        canvas.create_text(600, 150, text="CELULAR: ", font=("Arial", 14, "italic"), fill="white")
        canvas.create_text(90, 250, text="DIRECCIÓN: ", font=("Arial", 14, "italic"), fill="white")
        canvas.create_text(80, 400, text="MARCA: ", font=("Arial", 14, "italic"), fill="white")
        canvas.create_text(250, 400, text="MODELO: ", font=("Arial", 14, "italic"), fill="white")
        canvas.create_text(600, 400, text="TIPO DE APARATO: ", font=("Arial", 14, "italic"), fill="white")
        canvas.create_text(80, 500, text="FALLA: ", font=("Arial", 14, "italic"), fill="white")
        canvas.create_text(400, 500, text="SUBTOTAL: ", font=("Arial", 14, "bold"), fill="white")
        nit = tk.Entry(self, font=("Arial", 12), bg="white",fg="black" ,width=12)
        canvas.create_window(60, 175, window=nit)
        nombre = tk.Entry(self, font=("Arial", 12), bg="white", fg="black", width=40)
        canvas.create_window(340, 175, window=nombre)
        celular = tk.Entry(self, font=("Arial", 12), bg="white", fg="black", width=20)
        canvas.create_window(630, 175, window=celular)
        direccion = tk.Entry(self, font=("Arial", 12), bg="white", fg="black", width=30)
        canvas.create_window(140, 300, window=direccion)
        marca = tk.Entry(self, font=("Arial", 12), bg="white", fg="black", width=20)
        canvas.create_window(100, 450, window=marca)
        modelo = tk.Entry(self, font=("Arial", 12), bg="white", fg="black", width=15)
        canvas.create_window(280, 450, window=modelo)
        falla = tk.Entry(self, font=("Arial", 12), bg="white", fg="black", width=15)
        canvas.create_window(100, 550, window=falla)
        aparatos_validos = ["Televisor", "Radio", "Teatro en casa", "Herramienta", "Baterías"]
        tipo_aparato = tk.StringVar() #Aqui se guardara que tipo de aparato selecciono el usuario
        listado_aparatos = tk.OptionMenu(self, tipo_aparato, *aparatos_validos)
        canvas.create_window(600, 450, window=listado_aparatos)
        subTotal = tk.Label(self, text="Q.0", font=("Arial",12, "bold"), width=15, highlightthickness=3, highlightbackground="black")
        canvas.create_window(400, 550, window=subTotal)
        cancelar_B = tk.Button(self, text="CANCELAR",font=("Arial", 12, "bold"), command= self.ref_sub.volver_menu, bg="gray20", fg="white")
        canvas.create_window(590, 575, window=cancelar_B)
        generar_pdf = tk.Button(self, text="GENERAR PDF", font=("Arial", 12, "bold"),command=self.pdf ,bg="gray20", fg="white")
        canvas.create_window(730, 575, window=generar_pdf)

    def pdf(self):
        #Aqui el codigo que se ejecuta para guardar los datos
        pass

class BuscarHistorial(tk.Frame):
    def __init__(self, master, ref_sub):
        super().__init__(master, width=800, height=600)
        self.ref_sub = ref_sub
        self.pack_propagate(False)
        canvas = tk.Canvas(self, width=800, height=600)
        canvas.pack(fill="both", expand=True)
        aplicar_logo(canvas, "/home/erick/Documentos/ProyectoFinal/util/fondo.png")
        titulo = tk.Label(self, text="BÚSQUEDA POR NO. DE REFERENCIA:",font=("Arial", 14, "italic"),  width=50, height=2)
        canvas.create_window(400, 100, window=titulo)
        referencia = tk.Entry(self, font=("Arial", 12, "bold"))
        canvas.create_window(300, 200, window=referencia)
        buscar_B = tk.Button(self, text="BUSCAR", font=("Arial", 12, "bold"), bg="Slategray4", fg="black")
        canvas.create_window(500, 175, window=buscar_B)
        limpiar_B = tk.Button(self, text="LIMPIAR ", font=("Arial", 12, "bold"), bg="Slategray4", fg="black")
        canvas.create_window(500, 225, window=limpiar_B)
        canvas.create_rectangle(100, 275, 700,500, fill="white", outline="black")
        canvas.create_text(200, 300, text="DATOS CLIENTE:", font=("Arial", 12, "bold"))
        canvas.create_text(550, 300, text="FECHA: ", font=("Arial", 12, "bold"))
        canvas.create_text(205, 350, text="DATOS APARATO: ", font=("Arial", 12, "bold"))
        canvas.create_text(550, 400, text="ESTADO: ", font=("Arial", 12, "bold"))
        canvas.create_text(200, 400, text="ATENDIDO POR:", font=("Arial", 12, "bold"))
        canvas.create_text(550, 450, text="TOTAL: ", font=("Arial",12, "bold"))
        cancelar_B = tk.Button(self, text="CANCELAR", font=("Arial", 12, "bold"), command=  self.ref_sub.volver_menu,bg="gray20", fg="white")
        canvas.create_window(590, 575, window=cancelar_B)
        aceptar_B = tk.Button(self, text="ACEPTAR", font=("Arial", 12, "bold"), bg="gray20", fg="white")
        canvas.create_window(730, 575, window=aceptar_B)


class Bodega(tk.Frame):
    def __init__(self, master, ref_sub):
        super().__init__(master, width=800, height=600)
        self.ref_sub = ref_sub
        self.pack_propagate(False)
        canvas = tk.Canvas(self, width=800, height=600)
        canvas.pack(fill="both", expand=True)
        aplicar_logo(canvas, "/home/erick/Documentos/ProyectoFinal/util/fondo.png")
        titulo = tk.Label(self, text="BODEGA:", font=("Arial", 14, "italic"), width=50,height=2)
        canvas.create_window(400, 50, window=titulo)
        modelo_entrada = tk.Entry(self, font=("Arial", 14, "bold"))
        canvas.create_window(250, 95, window=modelo_entrada)
        aparatos_validos = ["Televisor", "Radio", "Teatro en casa", "Herramienta", "Baterías"]
        tipo_aparato = tk.StringVar()
        aparato_entrada = tk.OptionMenu(self, tipo_aparato, *aparatos_validos)
        canvas.create_window(250, 130, window=aparato_entrada)
        buscar_B = tk.Button(self, text="BUSCAR", font=("Arial", 12, "bold"),bg="Slategray4", fg="black", width=15, height=2)
        canvas.create_window(550, 110, window=buscar_B)
        canvas.create_rectangle(50, 150, 750, 550, fill="white", outline="gray")
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)
        contenedor = tk.Frame(canvas, bg="white")
        canvas_window = canvas.create_window((50, 200), window=contenedor, anchor="nw")
        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(canvas_window, width=700)  # Ajusta ancho del frame
        contenedor.bind("<Configure>", on_configure)
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))
        cancelar_B = tk.Button(self, text="CANCELAR", font=("Arial", 12, "bold"),command= self.ref_sub.volver_menu, bg="gray20", fg="white")
        canvas.create_window(590, 575, window=cancelar_B)
        aceptar_B = tk.Button(self, text="ACEPTAR", font=("Arial", 12, "bold"),bg="gray20", fg="white")
        canvas.create_window(730, 575, window=aceptar_B)


class Clientes(tk.Frame):
    def __init__(self, master, ref_sub):
        super().__init__(master, width=800, height=600)
        self.ref_sub = ref_sub
        self.pack_propagate(False)
        canvas = tk.Canvas(self, width=800, height=600)
        canvas.pack(fill="both", expand=True)
        aplicar_logo(canvas, "/home/erick/Documentos/ProyectoFinal/util/fondo.png")
        #buscar por nombre, nit o telefono
        titulo = tk.Label(self, text="BUSCAR CLIENTES: ", font=("Arial", 14, "italic"), width=50, height=2)
        canvas.create_window(400, 50, window=titulo)
        buscar_nombreB = tk.Button(self, text="Nombre", font=("Arial", 12, "bold"),bg="gray20", fg="white", width=10, height=2 )
        canvas.create_window(400, 150, window=buscar_nombreB)
        buscar_nitB = tk.Button(self, text="NIT", font=("Arial", 12, "bold"), bg="gray20", fg="white", width=10, height=2)
        canvas.create_window(500, 150, window=buscar_nitB)
        buscar_telefonoB = tk.Button(self, text="Teléfono", font=("Arial", 12, "bold"), bg="gray20", fg="white", width=10, height=2)
        canvas.create_window(600, 150, window=buscar_telefonoB)
        entrada = tk.Entry(self, font=("Arial", 12, "bold"))
        canvas.create_window(245,150, window=entrada)
        aceptar_B = tk.Button(self, text="ACEPTAR", font=("Arial", 12, "bold"), command=self.ref_sub.volver_menu, bg="gray20", fg="white")
        canvas.create_window(730, 575, window=aceptar_B)


class Cobros(tk.Frame):
    def __init__(self, master, ref_sub):
        super().__init__(master, width=800, height=600)
        self.ref_sub = ref_sub
        self.pack_propagate(False)
        canvas = tk.Canvas(self, width=800, height=600)
        canvas.pack(fill="both", expand=True)
        aplicar_logo(canvas,"/home/erick/Documentos/ProyectoFinal/util/fondo.png")
        titulo = tk.Label(self, text="BUSQUEDA COBROS: ", font=("Arial", 14, "italic"), width=50, height=2)
        canvas.create_window(400, 50, window=titulo)

        def actualizar_dias_desde(event):
            mes = meses.current() + 1
            year = int(anio.get())
            dias = [str(i) for i in range(1, calendar.monthrange(year, mes)[1] + 1)]
            dias_desde.config(values=dias)
            dias_desde.set("Día")

        etiqueta_desde = tk.Label(self, text="Desde:", font=("Arial", 14, "bold"), width=10, height=2)
        canvas.create_window(100, 100,window=etiqueta_desde)
        #Calendario para el desde
        anio = ttk.Combobox(self, values=[str(y) for y in range(2020, 2031)], width=6)
        anio.set("2025")
        canvas.create_window(80, 150, window=anio)
        meses = ttk.Combobox(self, values=list(calendar.month_name[1:]), width=10)
        meses.set("Mes")
        meses.bind("<<ComboboxSelected>>", actualizar_dias_desde)
        canvas.create_window(160, 150, window=meses)
        dias_desde = ttk.Combobox(self, values=[], width=5)
        dias_desde.set("Día")
        canvas.create_window(235, 150, window=dias_desde)


        def actualizar_dias_hasta(event):
            mes = meses.current() + 1
            year = int(anio.get())
            dias = [str(i) for i in range(1, calendar.monthrange(year, mes)[1] + 1)]
            dias_hasta.config(values=dias)
            dias_hasta.set("Día")

        #HASTA
        etiqueta_hasta = tk.Label(self, text="Hasta: ", font=("Arial", 14, "bold"), width=10, height=2)
        canvas.create_window(500, 100, window=etiqueta_hasta)
        #CALENDARIO HASTA
        anio_hasta = ttk.Combobox(self, values=[str(y) for y in range(2020, 2031)], width=6)
        anio_hasta.set("2025")
        canvas.create_window(480, 150, window=anio_hasta)
        meses_hasta = ttk.Combobox(self, values=list(calendar.month_name[1:]), width=10)
        meses_hasta.set("Mes")
        meses_hasta.bind("<<ComboboxSelected>>", actualizar_dias_hasta)
        canvas.create_window(560, 150, window=meses_hasta)
        dias_hasta = ttk.Combobox(self, values=[], width=5)
        dias_hasta.set("Día")
        canvas.create_window(635, 150, window=dias_hasta)

        boton_buscar = tk.Button(self, text="BUSCAR", font=("Arial", 12, "bold"), bg="gray20", fg="white")
        canvas.create_window(370, 200, window=boton_buscar)



        aceptar_B = tk.Button(self, text="ACEPTAR", font=("Arial", 12, "bold"), command=self.ref_sub.volver_menu, bg="gray20", fg="white")
        canvas.create_window(730, 575, window=aceptar_B)

class Trabajador(tk.Frame):
    def __init__(self, master, ref_sub):
        super().__init__(master, width=800, height=600)
        self.ref_sub = ref_sub
        self.pack_propagate(False)
        self.canvas = tk.Canvas(self, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)
        aplicar_logo(self.canvas, "/home/erick/Documentos/ProyectoFinal/util/fondo.png")
        titulo = tk.Label(self, text="TRABAJADOR: ", font=("Arial", 14, "italic"), width=50, height=2)
        self.canvas.create_window(400, 50, window=titulo)


        crear_trabajador = tk.Button(self, text="Crear Trabajador", font=("Arial",12, "bold"), bg="gray20", fg="white", width=20, height=2)
        self.canvas.create_window(400, 200, window=crear_trabajador)
        self.canvas.create_text(400, 250, text="Agrega información de nuevos trabajadores", font=("Arial", 14, "bold"), fill="white")
        listar_trabajador = tk.Button(self, text="Listar Trabajadores", font=("Arial", 12, "bold"), bg="gray20", fg="white", width=20, height=2)
        self.canvas.create_window(400,400, window=listar_trabajador)
        self.canvas.create_text(400, 450, text="Listado de todos los trabajadores contratados", font=("Arial", 14, "bold"), fill="white")

        aceptar_b = tk.Button(self, text="ACEPTAR", font=("Arial", 12, "bold"), command=self.ref_sub.volver_menu, bg="gray20", fg="white")
        self.canvas.create_window(730, 575, window=aceptar_b)









