import tkinter as tk
from PIL import Image, ImageTk

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
        canvas.create_text(530, 250, text="Usuario: ", font=("Arial", 14, "italic"), fill="white")
        #canvas.create_oval(100,100,350,200, fill="white", outline="black", width=2)
        canvas.create_text(550, 350, text="Contraseña: ", font=("Arial", 14, "italic"), fill="white")
        self.mostrar_contra = tk.BooleanVar()
        checkbox = tk.Checkbutton(canvas, text="Ver contraseña", variable=self.mostrar_contra, font=("Arial", 10, "italic"), bg="white")
        canvas.create_window(550, 450, window=checkbox)

        self.principal.mainloop()






if __name__ == "__main__":
    ProgramaTaller() #Se ejecuta lo que esta dentro de la clase

