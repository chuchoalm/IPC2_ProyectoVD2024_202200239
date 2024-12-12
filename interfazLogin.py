import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

#Element Tree
import xml.etree.ElementTree as ET
# Importar Tkinter para obtener la ruta de los archivos XML
from tkinter import filedialog, messagebox

from clases.Artista import Artista
from clases.Imagen import Imagen
from clases.Solicitante import Solicitante
#from clases.SolicitudCola import SolicitudCola
#from clases.SolicitudPila import SolicitudPila
#from estructuras.estructuras import (colaSolicitudes, id_logueado,
                                     #listaArtistas, listaSolicitantes)

# Función para manejar el inicio de sesión
def login():
    username = entry_username.get()
    password = entry_password.get()
    
    if username == "AdminIPC" and password == "ARTIPC2":
        messagebox.showinfo("Login", "Bienvenido Administrador")
        open_admin_window()
    elif username.startswith("ART-") and username[0:3] == "ART":
        messagebox.showinfo("Login", "Bienvenido Artista")
        open_artista_window()
    elif username.startswith("IPC-") and username[0:3] == "IPC":
        messagebox.showinfo("Login", "Bienvenido Solicitante")
        open_solicitante_window()
    else:
        messagebox.showerror("Error", "Credenciales incorrectas")

# Función para cerrar sesión y volver al login
def logout(window):
    window.destroy()
    entry_username.delete(0, tk.END)
    entry_password.delete(0, tk.END)
    root.deiconify()

# Función para abrir la ventana del administrador
def open_admin_window():
    root.withdraw()
    admin_window = tk.Toplevel(root)
    admin_window.title("Ventana Administrador")
    admin_window.geometry("800x600")
    
    tk.Label(admin_window, text="Bienvenido Administrador").pack(pady=20)
    tk.Button(admin_window, text="Cerrar Sesión", command=lambda: logout(admin_window)).place(x=570, y=10)

    tk.Button(admin_window, text="Cargar Solicitantes", command=cargar_solicitantes).pack(pady=5)
    tk.Button(admin_window, text="Cargar Artistas", command=cargar_artistas).pack(pady=5)
    tk.Button(admin_window, text="Ver Solicitantes", command=ver_solicitantes).pack(pady=5)
    tk.Button(admin_window, text="Ver Artistas", command=ver_artistas).pack(pady=5)
    
    # Espacio para mostrar artistas o solicitantes cargados
    global display_area
    display_area = tk.Text(admin_window, width=50, height=20)
    display_area.pack(pady=20)


# Función para abrir la ventana del artista
def open_artista_window():
    root.withdraw()
    artist_window = tk.Toplevel(root)
    artist_window.title("Panel de Artista")
    artist_window.geometry("800x600")
    
    tk.Label(artist_window, text="Bienvenido Artista").pack(pady=20)
    tk.Button(artist_window, text="Cerrar Sesión", command=lambda: logout(artist_window)).place(x=570, y=10)

# Función para abrir la ventana del solicitante
def open_solicitante_window():
    root.withdraw()
    applicant_window = tk.Toplevel(root)
    applicant_window.title("Ventana Solicitante")
    applicant_window.geometry("800x600")
    
    tk.Label(applicant_window, text="Bienvenido Solicitante").pack(pady=20)
    tk.Button(applicant_window, text="Cerrar Sesión", command=lambda: logout(applicant_window)).place(x=570, y=10)

# Funciones para cargar archivos .xml
def cargar_solicitantes():
    ruta = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
    if ruta:
        ruta_absoluta = ruta
        ruta_parcial = ruta.split("/")[-1]
        display_area.insert(tk.END, f"Solicitante cargado: {ruta_parcial}\n")

def cargar_artistas():
    ruta = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
    if ruta:
        ruta_absoluta = ruta
        ruta_parcial = ruta.split("/")[-1]
        display_area.insert(tk.END, f"Artista cargado: {ruta_parcial}\n")

# Funciones para ver artistas y solicitantes cargados (simulación)
def ver_solicitantes():
    display_area.insert(tk.END, "Mostrando solicitantes cargados...\n")

def ver_artistas():
    display_area.insert(tk.END, "Mostrando artistas cargados...\n")
    
# Ventana principal
root = tk.Tk()
root.title("Login")
root.geometry("600x350")

tk.Label(root, text="Usuario").pack(pady=10)
entry_username = tk.Entry(root)
entry_username.pack(pady=10)

tk.Label(root, text="Contraseña").pack(pady=10)
entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=10)

tk.Button(root, text="INGRESAR", command=login).pack(pady=20)

root.mainloop()
