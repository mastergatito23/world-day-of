import tkinter as tk
import customtkinter as ctk  # Importamos la librería para el lavado de cara
from PIL import Image, ImageTk 

# ==========================================
# Configuración de Estilo y Modo Oscuro
# ==========================================
ctk.set_appearance_mode("dark")  # Activa el Modo Oscuro por defecto ("dark" o "light")
ctk.set_default_color_theme("blue")  # Tema de color para los botones y acentos

root = ctk.CTk()  # Cambiado de tk.Tk() a ctk.CTk()
root.title("World Day Of")
root.geometry("600x350")  # Un poco más de altura para mejorar el espaciado
root.minsize(400, 250)

# Icono (Mantenemos tu lógica original)
try:
    ico = Image.open('test.jpg')
    photo = ImageTk.PhotoImage(ico)
    root.wm_iconphoto(False, photo)
except Exception as e:
    print(f"Icono no cargado: {e}")

# ==========================================
# Tipografía Mejorada y Layout
# ==========================================
# Título principal con mejor tipografía y espaciado
titulo = ctk.CTkLabel(
    root, 
    text="World Day Of", 
    font=("Segoe UI", 24, "bold"),  # Tipografía más moderna
    text_color="#FFFFFF"
)
titulo.pack(pady=(30, 10))  # Más espacio arriba para que respire

# Variable de texto para el subtítulo
variable_texto = tk.StringVar()
variable_texto.set("Welcome to World Day Of.\nCheck the world days by pressing the buttons.")

# Subtítulo con mejor padding y lectura
subtitulo = ctk.CTkLabel(
    root, 
    textvariable=variable_texto, 
    font=("Segoe UI", 14), 
    wraplength=500,
    text_color="#B0B0B0"  # Un tono grisáceo elegante para el texto secundario
)
subtitulo.pack(pady=(10, 30))

# ==========================================
# Lógica de los Botones
# ==========================================
def mostrar_ayer():
    variable_texto.set("Yesterday was: [Insertar Día]") 

def mostrar_hoy():
    variable_texto.set("Today is: [Insertar Día]") 

def mostrar_manana():
    variable_texto.set("Tomorrow will be: [Insertar Día]") 

# ==========================================
# Contenedor y Botones Redondeados
# ==========================================
# Usamos un CTkFrame transparente para alinear los botones
frame = ctk.CTkFrame(root, fg_color="transparent")
frame.pack(expand=True, fill="x", padx=40)

# Botón Izquierda (Yesterday)
btn_izquierda = ctk.CTkButton(
    frame, 
    text="Yesterday", 
    width=120, 
    height=45,
    corner_radius=12,  # ¡Esquinas redondeadas!
    font=("Segoe UI", 13, "bold"),
    command=mostrar_ayer
)
btn_izquierda.pack(side="left", expand=True, padx=10)

# Botón Medio (Today)
btn_medio = ctk.CTkButton(
    frame, 
    text="Today", 
    width=120, 
    height=45,
    corner_radius=12,
    font=("Segoe UI", 13, "bold"),
    command=mostrar_hoy
)
btn_medio.pack(side="left", expand=True, padx=10)

# Botón Derecha (Tomorrow)
btn_derecha = ctk.CTkButton(
    frame, 
    text="Tomorrow", 
    width=120, 
    height=45,
    corner_radius=12,
    font=("Segoe UI", 13, "bold"),
    command=mostrar_manana
)
btn_derecha.pack(side="left", expand=True, padx=10)

root.mainloop()