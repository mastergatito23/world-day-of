import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta
import calendar
import json
import os

# ==========================================
# CONFIG UI 🎮
# ==========================================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("World Day Of — v2.0 (Calendar View)")
root.geometry("750x650")
root.minsize(650, 550)

# ==========================================
# FILES & GLOBALS
# ==========================================
FAVORITES_FILE = "favorites.json"
SETTINGS_FILE = "settings.json"
ultimo_dia = None

# Variables para la navegación del calendario
anio_actual = datetime.now().year
mes_actual = datetime.now().month


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
# INTERACTIVE CALENDAR ENGINE 📅 (FIXED)
# ==========================================
def renderizar_calendario():
    global anio_actual, mes_actual
    
    # Limpiar matriz anterior del calendario
    for widget in frame_dias.winfo_children():
        widget.destroy()
        
    # Actualizar la etiqueta del mes/año actual
    nombre_mes = calendar.month_name[mes_actual]
    lbl_mes_anio.configure(text=f"📅 {nombre_mes} {anio_actual}")
    
    # Cabeceras de los días de la semana
    dias_semana = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    for col, dia_sem in enumerate(dias_semana):
        lbl = ctk.CTkLabel(frame_dias, text=dia_sem, font=("Segoe UI", 11, "bold"), text_color="gray")
        lbl.grid(row=0, column=col, pady=2)
        
    # Obtener matriz de días del mes
    cal = calendar.Calendar(firstweekday=0)
    semanas = cal.monthdayscalendar(anio_actual, mes_actual)
    
    hoy = datetime.now()
    
    for fila, semana in enumerate(semanas, start=1):
        # ¡CORREGIDO AQUÍ!: Se cambió "semanana" por "semana"
        for col, dia in enumerate(semana):
            if dia == 0:
                # Celda vacía para rellenar los desfases de días
                lbl_vacio = ctk.CTkLabel(frame_dias, text="")
                lbl_vacio.grid(row=fila, column=col)
            else:
                # Resaltar si es el día de hoy real en el sistema
                es_hoy = (dia == hoy.day and mes_actual == hoy.month and anio_actual == hoy.year)
                
                bg_color = "#1F6AA5" if es_hoy else "transparent"
                txt_color = "white" if es_hoy else "#E0E0E0"
                
                btn_dia = ctk.CTkButton(
                    frame_dias, 
                    text=str(dia),
                    width=35,
                    height=30,
                    fg_color=bg_color,
                    text_color=txt_color,
                    hover_color="#144870",
                    font=("Segoe UI", 11, "bold" if es_hoy else "normal"),
                    command=lambda d=dia: seleccionar_dia_calendario(d)
                )
                btn_dia.grid(row=fila, column=col, padx=2, pady=2)


def seleccionar_dia_calendario(dia):
    fecha_seleccionada = datetime(anio_actual, mes_actual, dia)
    mostrar_dia(fecha_seleccionada, "Selected Day")


def mes_anterior():
    global anio_actual, mes_actual
    mes_actual -= 1
    if mes_actual < 1:
        mes_actual = 12
        anio_actual -= 1
    renderizar_calendario()


def mes_siguiente():
    global anio_actual, mes_actual
    mes_actual += 1
    if mes_actual > 12:
        mes_actual = 1
        anio_actual += 1
    renderizar_calendario()


# ==========================================
# SEARCH ENGINE 🔍
# ==========================================
def ejecutar_busqueda(*args):
    termino = entrada_busqueda.get().strip().lower()
    caja_resultados.configure(state="normal")
    caja_resultados.delete("1.0", "end")
    
    if not termino:
        caja_resultados.insert("end", "Type a keyword or date to search...")
        caja_resultados.configure(state="disabled")
        return
        
    datos = cargar_base_datos()
    encontrados = 0
    
    for fecha_id, dia_nombre in datos.items():
        try:
            objeto_fecha = datetime.strptime(fecha_id, "%m-%d")
            fecha_legible = objeto_fecha.strftime("%B %d").lower()
        except:
            fecha_legible = ""
            
        if (termino in fecha_id or termino in dia_nombre.lower() or termino in fecha_legible):
            try:
                mes_dia_formato = datetime.strptime(fecha_id, "%m-%d").strftime("%B %d")
            except:
                mes_dia_formato = fecha_id
                
            caja_resultados.insert("end", f"📅 {mes_dia_formato} → {dia_nombre}\n\n")
            encontrados += 1
            
    if encontrados == 0:
        caja_resultados.insert("end", "❌ No World Days found.")
    caja_resultados.configure(state="disabled")


# ==========================================
# FAVORITES & SETTINGS SYSTEM ⭐🔔
# ==========================================
def cargar_favoritos():
    if not os.path.exists(FAVORITES_FILE): return []
    try:
        with open(FAVORITES_FILE, "r", encoding="utf-8") as f: return json.load(f)
    except: return []

def guardar_favoritos(data):
    with open(FAVORITES_FILE, "w", encoding="utf-8") as f: json.dump(data, f, indent=4, ensure_ascii=False)

def cargar_configuracion():
    if not os.path.exists(SETTINGS_FILE): return {"muted": False}
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f: return json.load(f)
    except: return {"muted": False}

def guardar_configuracion(config):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f: json.dump(config, f, indent=4, ensure_ascii=False)


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
        for f in favs: box.insert("end", f"⭐ {f}\n\n")
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
        btn_mute.configure(text="🔕 Unmute", fg_color="#E74C3C", hover_color="#C0392B")
    else:
        btn_mute.configure(text="🔔 Mute", fg_color="#2ECC71", hover_color="#27AE60")


def verificar_notificaciones():
    config = cargar_configuracion()
    if config.get("muted", False): return
    favs = cargar_favoritos()
    if not favs: return

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
                    alertas.append(f"• [{etiqueta}] 🎉 {partes[1]}")

    if alertas:
        messagebox.showinfo("🔔 World Day Reminder", "📅 Upcoming Favorite World Days:\n\n" + "\n".join(alertas))


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
# UI INTERFACE 🖥️
# ==========================================
titulo = ctk.CTkLabel(root, text="World Day Of 🌍", font=("Segoe UI", 24, "bold"))
titulo.pack(pady=10)

# Layout: Dividir en Izquierda (Info y Búsqueda) y Derecha (Calendario Interactivo)
frame_principal = ctk.CTkFrame(root, fg_color="transparent")
frame_principal.pack(expand=True, fill="both", padx=20, pady=10)

# ---- PANEL IZQUIERDO ----
panel_izquierdo = ctk.CTkFrame(frame_principal, fg_color="transparent")
panel_izquierdo.pack(side="left", expand=True, fill="both", padx=(0, 10))

variable_texto = tk.StringVar()
variable_texto.set("Click a date or button to explore 🌍")

lbl_display = ctk.CTkLabel(panel_izquierdo, textvariable=variable_texto, wraplength=320, font=("Segoe UI", 14), height=100)
lbl_display.pack(fill="x", pady=5)

frame_quick = ctk.CTkFrame(panel_izquierdo, fg_color="transparent")
frame_quick.pack(pady=5)
ctk.CTkButton(frame_quick, text="Yesterday", width=90, command=mostrar_ayer).pack(side="left", padx=2)
ctk.CTkButton(frame_quick, text="Today", width=90, command=mostrar_hoy).pack(side="left", padx=2)
ctk.CTkButton(frame_quick, text="Tomorrow", width=90, command=mostrar_manana).pack(side="left", padx=2)

# Sección de Búsqueda (Rediseñada abajo a la izquierda)
frame_search = ctk.CTkFrame(panel_izquierdo)
frame_search.pack(fill="both", expand=True, pady=10)
ctk.CTkLabel(frame_search, text="🔎 Quick Keyword Search:", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=10, pady=4)
entrada_busqueda = ctk.CTkEntry(frame_search, placeholder_text="Type keyword...", height=28)
entrada_busqueda.pack(fill="x", padx=10, pady=2)
entrada_busqueda.bind("<KeyRelease>", ejecutar_busqueda)
caja_resultados = ctk.CTkTextbox(frame_search, height=120)
caja_resultados.pack(fill="both", expand=True, padx=10, pady=5)
caja_resultados.insert("end", "Type a keyword to search...")
caja_resultados.configure(state="disabled")


# ---- PANEL DERECHO (CALENDARIO) 📅 ----
panel_derecho = ctk.CTkFrame(frame_principal, width=320)
panel_derecho.pack(side="right", fill="both", padx=(10, 0))

# Controles de navegación del calendario (Mes anterior / siguiente)
frame_nav_cal = ctk.CTkFrame(panel_derecho, fg_color="transparent")
frame_nav_cal.pack(fill="x", pady=10, padx=10)

btn_prev = ctk.CTkButton(frame_nav_cal, text="◀", width=30, command=mes_anterior)
btn_prev.pack(side="left")

lbl_mes_anio = ctk.CTkLabel(frame_nav_cal, text="Month Year", font=("Segoe UI", 15, "bold"))
lbl_mes_anio.pack(side="left", expand=True)

btn_next = ctk.CTkButton(frame_nav_cal, text="▶", width=30, command=mes_siguiente)
btn_next.pack(side="right")

# Contenedor para la rejilla de días (Grid)
frame_dias = ctk.CTkFrame(panel_derecho, fg_color="transparent")
frame_dias.pack(expand=True, padx=10, pady=5)


# ---- BARRA DE CONTROL INFERIOR ----
frame_bottom = ctk.CTkFrame(root, fg_color="transparent")
frame_bottom.pack(pady=15, fill="x", padx=20)
ctk.CTkButton(frame_bottom, text="⭐ Add Favorite", command=agregar_favorito).pack(side="left", padx=5, expand=True, fill="x")
ctk.CTkButton(frame_bottom, text="📂 View Favorites", command=mostrar_favoritos).pack(side="left", padx=5, expand=True, fill="x")
btn_mute = ctk.CTkButton(frame_bottom, text="🔔 Mute", command=alternar_silencio)
btn_mute.pack(side="left", padx=5, expand=True, fill="x")

# Inicialización general de UI y Lógica
renderizar_calendario()
config_inicial = cargar_configuracion()
actualizar_boton_mute(config_inicial.get("muted", False))
root.after(500, verificar_notificaciones)

root.mainloop()