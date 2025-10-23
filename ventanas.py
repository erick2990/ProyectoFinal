import tkinter as tk
from PIL import Image, ImageTk
from datetime import date

from cloudinit.util import center
from oauthlib.uri_validate import hier_part
from pygments import highlight
fecha = date.today()

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
        # Simulación de validación
        if usuario == "admin" and contra == "1234":
            self.root.withdraw()
            SubAdmin(self.root)
        elif usuario == "erick" and contra == "1234":
            self.root.withdraw()
            SubTrabajador(self.root)
        else:
            tk.messagebox.showerror("Error", "Credenciales incorrectas")

    def run(self):
        self.root.mainloop()


class SubTrabajador:

    def __init__(self, master):
        self.sub = tk.Toplevel(master)
        self.sub.title("TRABAJADOR")
        self.sub.geometry("800x600")
        canvas  = tk.Canvas(self.sub, width=800, height=600)
        canvas.pack(fill="both", expand=True)
        aplicar_logo(canvas, "/home/erick/Documentos/ProyectoFinal/util/fondo.png")
        registrar_aparatoB = tk.Button(self.sub, text="REGISTRAR\nAPARATO", font=("Arial", 14, "bold"), command=lambda:AgregarAparato(self.sub), highlightthickness=3, highlightbackground="blue4")
        canvas.create_window(100, 200, window = registrar_aparatoB)
        cotizar_B = tk.Button(self.sub, text="COTIZACIÓN DE\nREPARACIÓN", font=("Arial", 14, "bold"), command=lambda:Cotizacion(self.sub),highlightthickness=3, highlightbackground="blue4")
        canvas.create_window(400, 200 , window=cotizar_B)
        consulta_B = tk.Button(self.sub, text="CONSULTA DE\nREPARACIONES", font=("Arial", 14, "bold"), highlightthickness=3, highlightbackground="blue4")
        canvas.create_window(685,200, window=consulta_B)
        bodega_B = tk.Button(self.sub, text="BODEGA", font=("Arial", 14, "bold"), highlightthickness=3, highlightbackground="blue4", width=10, height=2)
        canvas.create_window(100, 300, window=bodega_B)
        buscar_B = tk.Button(self.sub, text="BUSCAR EN\nHISTORIAL", font=("Arial", 14, "bold"),command=lambda:BuscarHistorial(self.sub), highlightthickness=3, highlightbackground="blue4", width=15, height=2)
        canvas.create_window(400, 300, window=buscar_B)
        cerrar_B = tk.Button(self.sub, text="CERRAR SESIÓN", font=("Arial", 14, "bold"),command=self.cerrar_sesion, highlightthickness="3", highlightbackground="blue4", width=15, height=2)
        canvas.create_window(400, 500, window=cerrar_B)

    def cerrar_sesion(self):
        self.sub.destroy()
        self.sub.master.deiconify()

class SubAdmin:
    def __init__(self, master):
        self.sub = tk.Toplevel(master)
        self.sub.title("Administrador")
        self.sub.geometry("800x600")
        canvas = tk.Canvas(self.sub, width=800, height=600)
        canvas.pack(fill="both", expand=True)
        aplicar_logo(canvas, "/home/erick/Documentos/ProyectoFinal/util/fondo.png")
        trabajadores_B = tk.Button(self.sub, text="TRABAJADORES", font=("Arial",14, "bold"), highlightthickness=3, highlightbackground="blue4", width=15, height=2)
        canvas.create_window(100, 200, window=trabajadores_B)
        estadisticas_B = tk.Button(self.sub, text="ESTADISTICAS", font=("Arial", 14, "bold"), highlightthickness=3, highlightbackground="blue4", width=15, height=2)
        canvas.create_window(400, 200, window=estadisticas_B)
        consulta_B = tk.Button(self.sub, text="CONSULTA DE\nREPARACIONES" ,font=("Arial", 14, "bold"), highlightthickness=3, highlightbackground="blue4", width=15, height=2)
        canvas.create_window(700, 200, window=consulta_B)
        bodega_B = tk.Button(self.sub, text="BODEGA", font=("Arial", 14, "bold"), highlightthickness=3, highlightbackground="blue4", width=15, height=2)
        canvas.create_window(100, 300, window=bodega_B)
        clientes_B = tk.Button(self.sub, text="CLIENTES", font=("Arial", 14, "bold"), highlightthickness=3, highlightbackground="blue4", width=15, height=2)
        canvas.create_window(400, 300, window=clientes_B)
        cerrar_B = tk.Button(self.sub, text="Cerrar Sesión", font=("Arial",14,"bold"), command=self.cerrar_sesion, highlightthickness=3, highlightbackground="blue4", width=15, height=2)
        canvas.create_window(400, 500, window=cerrar_B)

    def cerrar_sesion(self):
        self.sub.destroy()
        self.sub.master.deiconify()

class AgregarAparato:
    def __init__(self, master):
        self.agregar = tk.Toplevel(master)
        self.agregar.title("AGREGAR APARATO")
        self.agregar.geometry("800x600")
        canvas = tk.Canvas(self.agregar, width=800, height=600)
        canvas.pack(fill="both", expand=True)
        aplicar_logo(canvas, "/home/erick/Documentos/ProyectoFinal/util/fondo.png")
        dato_etiqueta = tk.Label(self.agregar, text="DATOS CLIENTE: ", font=("Arial", 14, "bold"), width=20, height=2)
        canvas.create_window(100, 100, window=dato_etiqueta)
        detalles_etiqueta = tk.Label(self.agregar, text=" DETALLES APARATO: ", font=("Arial", 14, "bold"), width=20, height=2)
        canvas.create_window(100,350, window=detalles_etiqueta)
        fecha_etiqueta = tk.Label(self.agregar, text=f"{fecha.strftime("%d/%m/%y")}", font=("Arial", 12, "bold"), bg="white",width=10, height=2)
        canvas.create_window(600, 50, window=fecha_etiqueta)
        caso_etiqueta = tk.Label(self.agregar, text="No. 0000", font=("Arial", 12, "bold"), bg="white", width=10, height=2)
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
        nit = tk.Entry(self.agregar, font=("Arial", 12), bg="white",fg="black" ,width=12)
        canvas.create_window(60, 175, window=nit)
        nombre = tk.Entry(self.agregar, font=("Arial", 12), bg="white", fg="black", width=40)
        canvas.create_window(340, 175, window=nombre)
        celular = tk.Entry(self.agregar, font=("Arial", 12), bg="white", fg="black", width=20)
        canvas.create_window(630, 175, window=celular)
        direccion = tk.Entry(self.agregar, font=("Arial", 12), bg="white", fg="black", width=30)
        canvas.create_window(60, 300, window=direccion)
        marca = tk.Entry(self.agregar, font=("Arial", 12), bg="white", fg="black", width=20)
        canvas.create_window(80, 450, window=marca)
        modelo = tk.Entry(self.agregar, font=("Arial", 12), bg="white", fg="black", width=15)
        canvas.create_window(280, 450, window=modelo)
        falla = tk.Entry(self.agregar, font=("Arial", 12), bg="white", fg="black", width=15)
        canvas.create_window(100, 550, window=falla)
        aparatos_validos = ["Televisor", "Radio", "Teatro en casa", "Herramienta", "Baterías"]
        tipo_aparato = tk.StringVar() #Aqui se guardara que tipo de aparato selecciono el usuario
        listado_aparatos = tk.OptionMenu(self.agregar, tipo_aparato, *aparatos_validos)
        canvas.create_window(600, 450, window=listado_aparatos)
        subTotal = tk.Label(self.agregar, text="Q.0", font=("Arial",12, "bold"), width=15, highlightthickness=3, highlightbackground="black")
        canvas.create_window(400, 550, window=subTotal)
        cancelar_B = tk.Button(self.agregar, text="CANCELAR",font=("Arial", 12, "bold"), command= self.cancelar, bg="gray20", fg="white")
        canvas.create_window(600, 575, window=cancelar_B)
        aceptar_B = tk.Button(self.agregar, text="ACEPTAR", font=("Arial", 12, "bold"),command=self.aceptar ,bg="gray20", fg="white")
        canvas.create_window(725, 575, window=aceptar_B)

    def cancelar(self):
        self.agregar.destroy()

    def aceptar(self):
        #Aqui el codigo que se ejecuta para guardar los datos
        pass

class Cotizacion:
    def __init__(self, master):
        self.coti = tk.Toplevel(master)
        self.coti.title("COTIZACIÓN DE REPARACIÓN")
        self.coti.geometry("800x600")
        canvas = tk.Canvas(self.coti, width=800, height=600)
        canvas.pack(fill="both", expand=True)
        aplicar_logo(canvas, "/home/erick/Documentos/ProyectoFinal/util/fondo.png")
        dato_etiqueta = tk.Label(self.coti, text="DATOS CLIENTE: ", font=("Arial", 14, "bold"), width=20, height=2)
        canvas.create_window(100, 100, window=dato_etiqueta)
        detalles_etiqueta = tk.Label(self.coti, text=" DETALLES APARATO: ", font=("Arial", 14, "bold"), width=20, height=2)
        canvas.create_window(100,350, window=detalles_etiqueta)
        fecha_etiqueta = tk.Label(self.coti, text=f"{fecha.strftime("%d/%m/%y")}", font=("Arial", 12, "bold"), bg="white",width=10, height=2)
        canvas.create_window(600, 50, window=fecha_etiqueta)
        caso_etiqueta = tk.Label(self.coti, text="No. 0000", font=("Arial", 12, "bold"), bg="white", width=10, height=2)
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
        nit = tk.Entry(self.coti, font=("Arial", 12), bg="white",fg="black" ,width=12)
        canvas.create_window(60, 175, window=nit)
        nombre = tk.Entry(self.coti, font=("Arial", 12), bg="white", fg="black", width=40)
        canvas.create_window(340, 175, window=nombre)
        celular = tk.Entry(self.coti, font=("Arial", 12), bg="white", fg="black", width=20)
        canvas.create_window(630, 175, window=celular)
        direccion = tk.Entry(self.coti, font=("Arial", 12), bg="white", fg="black", width=30)
        canvas.create_window(60, 300, window=direccion)
        marca = tk.Entry(self.coti, font=("Arial", 12), bg="white", fg="black", width=20)
        canvas.create_window(80, 450, window=marca)
        modelo = tk.Entry(self.coti, font=("Arial", 12), bg="white", fg="black", width=15)
        canvas.create_window(280, 450, window=modelo)
        falla = tk.Entry(self.coti, font=("Arial", 12), bg="white", fg="black", width=15)
        canvas.create_window(100, 550, window=falla)
        aparatos_validos = ["Televisor", "Radio", "Teatro en casa", "Herramienta", "Baterías"]
        tipo_aparato = tk.StringVar() #Aqui se guardara que tipo de aparato selecciono el usuario
        listado_aparatos = tk.OptionMenu(self.coti, tipo_aparato, *aparatos_validos)
        canvas.create_window(600, 450, window=listado_aparatos)
        subTotal = tk.Label(self.coti, text="Q.0", font=("Arial",12, "bold"), width=15, highlightthickness=3, highlightbackground="black")
        canvas.create_window(400, 550, window=subTotal)
        cancelar_B = tk.Button(self.coti, text="CANCELAR",font=("Arial", 12, "bold"), command= self.cancelar, bg="gray20", fg="white")
        canvas.create_window(590, 575, window=cancelar_B)
        generar_pdf = tk.Button(self.coti, text="GENERAR PDF", font=("Arial", 12, "bold"),command=self.pdf ,bg="gray20", fg="white")
        canvas.create_window(730, 575, window=generar_pdf)

    def cancelar(self):
        self.coti.destroy()

    def pdf(self):
        #Aqui el codigo que se ejecuta para guardar los datos
        pass

class BuscarHistorial:
    def __init__(self, master):
        self.buscar = tk.Toplevel(master)
        self.buscar.title("BUSCAR EN HISTORIAL")
        self.buscar.geometry("800x600")
        canvas = tk.Canvas(self.buscar, width=800, height=600)
        canvas.pack(fill="both", expand=True)
        aplicar_logo(canvas, "/home/erick/Documentos/ProyectoFinal/util/fondo.png")
        titulo = tk.Label(self.buscar, text="BÚSQUEDA POR NO. DE REFERENCIA:",font=("Arial", 12, "bold"),  width=50, height=2)
        canvas.create_window(400, 100, window=titulo)
        referencia = tk.Entry(self.buscar, font=("Arial", 12, "bold"))
        canvas.create_window(200, 200, window=referencia)









