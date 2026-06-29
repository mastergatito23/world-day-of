import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta
import json
import os

# ==========================================
# CONFIG UI 🎮
# ==========================================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("World Day Of — v1.7 (Search)")
root.geometry("650x550")
root.minsize(500, 400)

# ==========================================
# FILES
# ==========================================
FAVORITES_FILE = "favorites.json"
SETTINGS_FILE = "settings.json"
ultimo_dia = None


# ==========================================
# DATA SYSTEM 🌍
# ==========================================
def cargar_base_datos():
    try:
        with open("dias_mundiales.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return {}


def obtener_dia_mundial(fecha):
    formato = fecha.strftime("%m-%d")
    datos = cargar_base_datos()
    
    if not datos:
        return "Database (JSON) not found or empty."
    
    if formato in datos:
        return datos[formato].replace(" / ", "\n")
    return "No special World Day registered for this date."


# ==========================================
# SEARCH SYSTEM 🔍 (NEW v1.7)
# ==========================================
def ejecutar_busqueda(*args):
    termino = entrada_busqueda.get().strip().lower()
    caja_resultados.configure(state="normal")
    caja_resultados.delete("1.0", "end")
    
    if not termino:
        caja_resultados.insert("end", "Type a keyword or date (e.g., 'Water' or '03-22') to search...")
        caja_resultados.configure(state="disabled")
        return
        
    datos = cargar_base_datos()
    encontrados = 0
    
    for fecha_id, dia_nombre in datos.items():
        # Intentar convertir la fecha ID (03-22) a formato legible (March 22) para ampliar la búsqueda
        try:
            objeto_fecha = datetime.strptime(fecha_id, "%m-%d")
            fecha_legible = objeto_fecha.strftime("%B %d").lower()
        except:
            fecha_legible = ""
            
        # Comprobar si coincide con la clave, el nombre del día o el formato legible
        if (termino in fecha_id or 
            termino in dia_nombre.lower() or 
            termino in fecha_legible):
            
            try:
                mes_dia_formato = datetime.strptime(fecha_id, "%m-%d").strftime("%B %d")
            except:
                mes_dia_formato = fecha_id
                
            caja_resultados.insert("end", f"📅 {mes_dia_formato} → {dia_nombre}\n\n")
            encontrados += 1
            
    if encontrados == 0:
        caja_resultados.insert("end", "❌ No World Days found matching your search.")
        
    caja_resultados.configure(state="disabled")


# ==========================================
# FAVORITES & SETTINGS SYSTEM ⭐🔔
# ==========================================
def cargar_favoritos():
    if not os.path.exists(FAVORITES_FILE):
        return []
    try:
        with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def guardar_favoritos(data):
    with open(FAVORITES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def cargar_configuracion():
    if not os.path.exists(SETTINGS_FILE):
        return {"muted": False}
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"muted": False}


def guardar_configuracion(config):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)


def agregar_favorito():
    global ultimo_dia

    if not ultimo_dia:
        variable_texto.set("Open a World Day first ⚠️")
        return

    favs = cargar_favoritos()

    if ultimo_dia not in favs:
        favs.append(ultimo_dia)
        guardar_favoritos(favs)
        variable_texto.set(variable_texto.get() + "\n\n⭐ Added to favorites!")
    else:
        variable_texto.set(variable_texto.get() + "\n\n⭐ Already in favorites!")


def mostrar_favoritos():
    ventana = ctk.CTkToplevel(root)
    ventana.title("Favorites ⭐")
    ventana.geometry("500x400")
    ventana.after(100, lambda: ventana.focus())

    title = ctk.CTkLabel(ventana, text="⭐ Your Favorite World Days", font=("Segoe UI", 18, "bold"))
    title.pack(pady=10)

    box = ctk.CTkTextbox(ventana)
    box.pack(expand=True, fill="both", padx=15, pady=10)

    favs = cargar_favoritos()
    if favs:
        for f in favs:
            box.insert("end", f"⭐ {f}\n\n")
    else:
        box.insert("end", "No favorites yet 😢")

    box.configure(state="disabled")


def alternar_silencio():
    config = cargar_configuracion()
    config["muted"] = not config["muted"]
    guardar_configuracion(config)
    actualizar_boton_mute(config["muted"])


def actualizar_boton_mute(is_muted):
    if is_muted:
        btn_mute.configure(text="🔕 Unmute Notifications", fg_color="#E74C3C", hover_color="#C0392B")
    else:
        btn_mute.configure(text="🔔 Mute Notifications", fg_color="#2ECC71", hover_color="#27AE60")


def verificar_notificaciones():
    config = cargar_configuracion()
    if config.get("muted", False):
        return

    favs = cargar_favoritos()
    if not favs:
        return

    ahora = datetime.now()
    fechas_a_revisar = {
        0: (ahora.strftime("%B %d"), "Today"),
        1: ((ahora + timedelta(days=1)).strftime("%B %d"), "Tomorrow"),
        2: ((ahora + timedelta(days=2)).strftime("%B %d"), "In 2 days")
    }

    alertas = []
    for dias_de_distancia, (fecha_str, etiqueta) in fechas_a_revisar.items():
        for fav in favs:
            if fav.startswith(fecha_str):
                partes = fav.split("\n")
                if len(partes) > 1:
                    nombre_dia = partes[1]
                    alertas.append(f"• [{etiqueta}] 🎉 {nombre_dia}")

    if alertas:
        alert_text = "📅 Upcoming Favorite World Days:\n\n" + "\n".join(alertas)
        messagebox.showinfo("🔔 World Day Reminder", alert_text)


# ==========================================
# DISPLAY LOGIC 📅
# ==========================================
def mostrar_dia(fecha, label):
    global ultimo_dia

    dia_texto = obtener_dia_mundial(fecha)
    fecha_legible = fecha.strftime("%B %d")
    ultimo_dia = f"{fecha_legible}\n{dia_texto.replace(chr(10), ' / ')}"

    if "not found" in dia_texto or "Error" in dia_texto:
        variable_texto.set(dia_texto)
    elif "No special" in dia_texto:
        variable_texto.set(f"{label} ({fecha_legible})\nNo World Day found.")
    else:
        variable_texto.set(f"{label} ({fecha_legible}) is:\n\n🌍 {dia_texto}")


def mostrar_ayer(): mostrar_dia(datetime.now() - timedelta(days=1), "Yesterday")
def mostrar_hoy(): mostrar_dia(datetime.now(), "Today")
def mostrar_manana(): mostrar_dia(datetime.now() + timedelta(days=1), "Tomorrow")


# ==========================================
# UI 🖥️
# ==========================================
titulo = ctk.CTkLabel(root, text="World Day Of 🌍", font=("Segoe UI", 24, "bold"))
titulo.pack(pady=15)

variable_texto = tk.StringVar()
variable_texto.set("Click a button to explore World Days 🌍")

subtitulo = ctk.CTkLabel(root, textvariable=variable_texto, wraplength=500, font=("Segoe UI", 13))
subtitulo.pack(pady=5)

# Quick look buttons
frame_quick = ctk.CTkFrame(root, fg_color="transparent")
frame_quick.pack(pady=5)
ctk.CTkButton(frame_quick, text="Yesterday", width=100, command=mostrar_ayer).pack(side="left", padx=5)
ctk.CTkButton(frame_quick, text="Today", width=100, command=mostrar_hoy).pack(side="left", padx=5)
ctk.CTkButton(frame_quick, text="Tomorrow", width=100, command=mostrar_manana).pack(side="left", padx=5)

# --- SEARCH SECTION 🔍 ---
frame_search = ctk.CTkFrame(root)
frame_search.pack(fill="x", padx=20, pady=15)

lbl_search = ctk.CTkLabel(frame_search, text="🔎 Search World Days:", font=("Segoe UI", 12, "bold"))
lbl_search.pack(anchor="w", padx=15, pady=(5, 0))

entrada_busqueda = ctk.CTkEntry(frame_search, placeholder_text="Type keyword (e.g. 'Science') or date (e.g. '11-10')...")
entrada_busqueda.pack(fill="x", padx=15, pady=5)
entrada_busqueda.bind("<KeyRelease>", ejecutar_busqueda) # Búsqueda instantánea en tiempo real

caja_resultados = ctk.CTkTextbox(frame_search, height=120)
caja_resultados.pack(fill="x", padx=15, pady=(0, 10))
caja_resultados.insert("end", "Type a keyword or date (e.g., 'Water' or '03-22') to search...")
caja_resultados.configure(state="disabled")

# Favorites & Mute controls
frame_bottom = ctk.CTkFrame(root, fg_color="transparent")
frame_bottom.pack(pady=5)
ctk.CTkButton(frame_bottom, text="⭐ Add Favorite", command=agregar_favorito).pack(side="left", padx=5)
ctk.CTkButton(frame_bottom, text="📂 Favorites", command=mostrar_favoritos).pack(side="left", padx=5)
btn_mute = ctk.CTkButton(frame_bottom, text="🔔 Mute Notifications", command=alternar_silencio)
btn_mute.pack(side="left", padx=5)

# Init config
config_inicial = cargar_configuracion()
actualizar_boton_mute(config_inicial.get("muted", False))
root.after(500, verificar_notificaciones)

root.mainloop()