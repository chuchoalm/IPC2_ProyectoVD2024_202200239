import tkinter as tk
from tkinter import messagebox

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
