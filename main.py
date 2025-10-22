import tkinter as tk
from PIL import Image, ImageTk
from requests import session
from yaml import compose_all
import ventanas
from ventanas import Login

if __name__ == "__main__":
    app = Login()
    app.run()

