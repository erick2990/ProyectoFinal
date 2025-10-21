import tkinter as tk
from PIL import Image, ImageTk
from requests import session
from yaml import compose_all


class ProgramaTaller:
    def __init__(self):
        self.principal = tk.Tk()
        self.principal.title("TALLER ELECTRÓNICO")
        self.principal.geometry("800x600")

        canvas = tk.Canvas(self.principal, width=800, height=600, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        fondo = Image.open("/home/erick/Documentos/ProyectoFinal/util/fondo.png")
        fondo = fondo.resize((800, 600))
        fondo_tk = ImageTk.PhotoImage(fondo)
        canvas.create_image(0, 0, anchor="nw", image=fondo_tk)
        canvas.fondo_img = fondo_tk

        logotipo = Image.open("/home/erick/Documentos/ProyectoFinal/util/Logotipo.png").convert("RGBA")
        logotipo = logotipo.resize((350, 350))
        logo_tk = ImageTk.PhotoImage(logotipo)
        canvas.create_image(250, 250, anchor="center", image=logo_tk)
        canvas.logo_img = logo_tk
        canvas.create_text(600, 150, text="Inicio de sesión", font=("Arial", 14, "bold"), fill="white")
        canvas.create_text(530, 200, text="Usuario: ", font=("Arial", 14, "italic"), fill="white")
        canvas.create_text(550, 300, text="Contraseña: ", font=("Arial", 14, "italic"), fill="white")

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


        boton_iniciar = tk.Button(canvas, text="Iniciar Sesión", font=("Arial", 12, "bold"), bg="RoyalBlue4", fg="white")
        canvas.create_window(600, 450, window=boton_iniciar)

        self.principal.mainloop()






if __name__ == "__main__":
    ProgramaTaller() #Se ejecuta lo que esta dentro de la clase

