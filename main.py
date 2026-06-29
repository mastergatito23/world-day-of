import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk 
import json
from datetime import datetime, timedelta

# ==========================================
# Configuración de Estilo y Modo Oscuro
# ==========================================
ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("blue")  

root = ctk.CTk()  
root.title("World Day Of v1.5")
root.geometry("600x350")  
root.minsize(400, 250)


# ==========================================
# Lógica de Datos (JSON & Datetime)
# ==========================================

def obtener_dia_mundial(fecha):
    """Busca en el JSON el día mundial según el formato MM-DD"""
    formato_busqueda = fecha.strftime("%m-%d") # Transforma la fecha a "MM-DD"
    
    try:
        with open("dias_mundiales.json", "r", encoding="utf-8") as f:
            datos = json.load(f)
        
        if formato_busqueda in datos:
            # Reemplaza la barra diagonal por un salto de línea real
            return datos[formato_busqueda].replace(" / ", "\n")
        else:
            return "No special World Day registered for this date."
            
    except FileNotFoundError:
        return "Database (JSON) not found."
    except Exception as e:
        return f"Error loading data: {e}"

# ==========================================
# Acciones de los Botones Actualizadas
# ==========================================

def mostrar_ayer():
    ayer = datetime.now() - timedelta(days=1)
    dia_texto = obtener_dia_mundial(ayer)
    fecha_legible = ayer.strftime("%B %d")
    
    # Si no hay día especial, adaptamos el texto para que quede natural
    if "not found" in dia_texto or "Error" in dia_texto:
        variable_texto.set(dia_texto) # Muestra el error de base de datos directamente
    elif dia_texto == "No special World Day registered for this date.":
        variable_texto.set(f"Yesterday ({fecha_legible})\nThere was no official World Day registered.")
    else:
        variable_texto.set(f"Yesterday ({fecha_legible}) was:\n\n🌍 {dia_texto}") 

def mostrar_hoy():
    hoy = datetime.now()
    dia_texto = obtener_dia_mundial(hoy)
    fecha_legible = hoy.strftime("%B %d")
    
    if "not found" in dia_texto or "Error" in dia_texto:
        variable_texto.set(dia_texto)
    elif dia_texto == "No special World Day registered for this date.":
        variable_texto.set(f"Today ({fecha_legible})\nThere is no official World Day registered.")
    else:
        variable_texto.set(f"Today ({fecha_legible}) is:\n\n🌍 {dia_texto}") 

def mostrar_manana():
    manana = datetime.now() + timedelta(days=1)
    dia_texto = obtener_dia_mundial(manana)
    fecha_legible = manana.strftime("%B %d")
    
    if "not found" in dia_texto or "Error" in dia_texto:
        variable_texto.set(dia_texto)
    elif dia_texto == "No special World Day registered for this date.":
        variable_texto.set(f"Tomorrow ({fecha_legible})\nThere will be no official World Day registered.")
    else:
        variable_texto.set(f"Tomorrow ({fecha_legible}) will be:\n\n🌍 {dia_texto}")

# ==========================================
# Interfaz Gráfica (UI)
# ==========================================

titulo = ctk.CTkLabel(
    root, 
    text="World Day Of", 
    font=("Segoe UI", 24, "bold"),  
    text_color="#FFFFFF"
)
titulo.pack(pady=(30, 10))  

variable_texto = tk.StringVar()
variable_texto.set("Welcome to World Day Of.\nCheck the world days by pressing the buttons.")

subtitulo = ctk.CTkLabel(
    root, 
    textvariable=variable_texto, 
    font=("Segoe UI", 14), 
    wraplength=500,
    text_color="#B0B0B0"  
)
subtitulo.pack(pady=(10, 30))

# Contenedor de Botones
frame = ctk.CTkFrame(root, fg_color="transparent")
frame.pack(expand=True, fill="x", padx=40)

# Botones
btn_izquierda = ctk.CTkButton(
    frame, text="Yesterday", width=120, height=45, corner_radius=12,
    font=("Segoe UI", 13, "bold"), command=mostrar_ayer
)
btn_izquierda.pack(side="left", expand=True, padx=10)

btn_medio = ctk.CTkButton(
    frame, text="Today", width=120, height=45, corner_radius=12,
    font=("Segoe UI", 13, "bold"), command=mostrar_hoy
)
btn_medio.pack(side="left", expand=True, padx=10)

btn_derecha = ctk.CTkButton(
    frame, text="Tomorrow", width=120, height=45, corner_radius=12,
    font=("Segoe UI", 13, "bold"), command=mostrar_manana
)
btn_derecha.pack(side="left", expand=True, padx=10)

root.mainloop()