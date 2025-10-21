import tkinter as tk
from PIL import Image, ImageTk

class Submenu:
    def __init__(self):
        self.sub = tk.Tk()
        self.sub.title("SUBMENÚ")
        self.sub.geometry("800x600")

        self.canvas = tk.Canvas(self.sub, width=800, height=600, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        fondo = Image.open("/home/erick/Documentos/ProyectoFinal/util/fondo.png")
        fondo = fondo.resize((800, 600))
        fondo_tk = ImageTk.PhotoImage(fondo)
        self.canvas.create_image(0, 0, anchor="nw", image=fondo_tk)
        self.canvas.fondo_img = fondo_tk

        salir_boton = tk.Button(self.canvas, text="SALIR",command=quit,font=("Arial", 14, "bold"), highlightbackground="blue4", highlightthickness=3 )
        self.canvas.create_window(400, 500, window=salir_boton)
        #self.sub.mainloop()

class Subadmin(Submenu):

    def __init__(self):
        super().__init__()
        self.sub.title("TRABAJADOR")
        registrar_aparatoB = tk.Button(self.sub, text="REGISTRAR\nAPARATO", font=("Arial", 14, "bold"), highlightthickness=3, highlightbackground="blue4")
        self.canvas.create_window(100, 200, window = registrar_aparatoB)
        cotizar_B = tk.Button(self.sub, text="COTIZACIÓN DE\nREPARACIÓN", font=("Arial", 14, "bold"), highlightthickness=3, highlightbackground="blue4")
        self.canvas.create_window(400, 200 , window=cotizar_B)




        self.sub.mainloop()



# Para probarlo directamente
if __name__ == "__main__":
    Subadmin()
