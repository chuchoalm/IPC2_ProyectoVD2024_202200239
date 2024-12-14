import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
#Element Tree
import xml.etree.ElementTree as ET
# Importar Tkinter para obtener la ruta de los archivos XML
from tkinter import filedialog, messagebox
from estructuras.lista_doble.listaDoble import ListaDoble
from clases.Artista import Artista
from clases.Imagen import Imagen
from clases.Solicitante import Solicitante
from clases.SolicitudCola import SolicitudCola
from estructuras.matrizDispersa.matrizDispersa import MatrizDispersa
from clases.SolicitudPila import SolicitudPila
from estructuras.estructuras import (colaSolicitudes, id_logueado,
                                     listaArtistas, listaSolicitantes)

# Función para manejar el inicio de sesión
def login():
    global id_logueado
    id = entry_username.get()
        
    pwd = entry_password.get()
       
    if id == "AdminIPC" and pwd == "ARTIPC2":
            messagebox.showinfo("Login", "Bienvenido Administrador")
            open_admin_window()
    elif id.startswith("ART-") and id[0:3] == "ART" and listaArtistas.loginUsuario(id,pwd) == True:
            messagebox.showinfo("Login", "Bienvenido Artista")
            id_logueado = id
            open_artista_window()
    elif id.startswith("IPC-") and id[0:3] == "IPC"and listaSolicitantes.login(id,pwd) == True:
            id_logueado = id
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
    global id_logueado
    root.withdraw()
    artist_window = tk.Toplevel(root)
    artist_window.title("Panel de Artista")
    artist_window.geometry("800x600")
    
    tk.Label(artist_window, text="Bienvenido Artista "+ id_logueado).pack(pady=20)
    tk.Button(artist_window, text="Cerrar Sesión", command=lambda: logout(artist_window)).place(x=570, y=10)

    frame = tk.Frame(artist_window)
    frame.pack(pady=20)

    tk.Button(frame, text="Aceptar").grid(row=0, column=0, pady=5)
    tk.Button(frame, text="Ver Cola").grid(row=1, column=0, pady=5)
    tk.Button(frame, text="Imágenes Procesadas").grid(row=2, column=0, pady=5)

    # Espacio para mostrar texto
    global text_display_area
    text_display_area = tk.Text(frame, width=30, height=10)
    text_display_area.grid(row=0, column=1, rowspan=3, padx=10)

    # Espacio para mostrar imágenes
    global image_display_area
    image_display_area = tk.Label(frame)
    image_display_area.grid(row=0, column=2, rowspan=3, padx=10)


def AceptarSolicitud():
    global id_logueado
    solicitud = colaSolicitudes.verPrimero()
    if solicitud == None:
        return
    #LO SACAMOS DE LA COLA
    solicitud_aceptada = colaSolicitudes.dequeue()
    #INSERTAN EN LA LISTA CIRCULAR
    listaArtistas.insertarProcesados(id_logueado,solicitud_aceptada)
    #GENERAMOS LA FIGURA
    matriz_figura = MatrizDispersa()
    #PARSEAR EL XML
    tree = ET.parse(solicitud_aceptada.ruta_xml)
    #Obtengo el elemento raiz
    root = tree.getroot()
    nombre_figura = ''
    for elemento in root:
        if elemento.tag == 'diseño':
            for pixel in elemento:
                fila = int(pixel.attrib['fila'])
                columna = int(pixel.attrib['col'])
                color = pixel.text
                matriz_figura.insertar(fila,columna,color)
        elif elemento.tag == 'nombre':
            nombre_figura = elemento.text

    
    #GRAFICAMOS
    ruta = matriz_figura.graficar(solicitud_aceptada.id)
    #creamos el nuevo objeto imagen para insertarlo a la lista doble del usuario
    nueva_imagen = Imagen(solicitud_aceptada.id,nombre_figura,ruta)
    #insertamos el objeto a la lista doble del usuario
    listaSolicitantes.insertarImagenUsuario(solicitud_aceptada.id_solicitante,nueva_imagen)



# Función para abrir la ventana del solicitante
def open_solicitante_window():
    global id_logueado
    root.withdraw()
    applicant_window = tk.Toplevel(root)
    applicant_window.title("Ventana Solicitante")
    applicant_window.geometry("800x600")
    
    tk.Label(applicant_window, text="Bienvenido Solicitante " + id_logueado).pack(pady=20)
    tk.Button(applicant_window, text="Cerrar Sesión", command=lambda: logout(applicant_window)).place(x=570, y=10)

     # Frame para los botones y áreas de visualización
    frame = tk.Frame(applicant_window)
    frame.pack(pady=20)

    # Botones para solicitar, ver galería, cargar figura, ver pila y ver lista
    tk.Button(frame, text="Solicitar").grid(row=0, column=0, pady=5)
    tk.Button(frame, text="Ver Galería", command=open_gallery_window).grid(row=1, column=0, pady=5)
    tk.Button(frame, text="Cargar Figura").grid(row=2, column=0, pady=5)
    tk.Button(frame, text="Ver Pila", command=ver_pila).grid(row=3, column=0, pady=5)
    tk.Button(frame, text="Ver Lista", command=ver_lista).grid(row=4, column=0, pady=5)

    # Espacio para mostrar imágenes
    global applicant_image_display_area
    applicant_image_display_area = tk.Label(frame)
    applicant_image_display_area.grid(row=0, column=1, rowspan=5, padx=10)

# Función para abrir la ventana de galería
def open_gallery_window():
    gallery_window = tk.Toplevel(root)
    gallery_window.title("Galería")
    gallery_window.geometry("900x600")

    # Frame para los botones y área de visualización
    frame = tk.Frame(gallery_window)
    frame.pack(pady=20)

    # Botones de navegación y espacio para mostrar imágenes
    tk.Button(frame, text="Anterior").grid(row=0, column=0, pady=5)
    tk.Button(frame, text="Siguiente").grid(row=0, column=2, pady=5)
    global gallery_image_display_area
    gallery_image_display_area = tk.Label(frame)
    gallery_image_display_area.grid(row=0, column=1, padx=10)

# Función para ver pila
def ver_pila():
    ruta = "./Reportes/Pila_IDSolicitante.svg"
    cargar_imagen(ruta, applicant_image_display_area)

# Función para ver lista
def ver_lista():
    ruta = "./Reportes/Lista_Doble_IDSolicitante.svg"
    cargar_imagen(ruta, applicant_image_display_area)

# Función para cargar imágenes
def cargar_imagen(ruta, display_area):
    try:
        img = Image.open(ruta)
        img = img.resize((300, 300), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        display_area.config(image=img)
        display_area.image = img
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")


# Funciones para cargar archivos .xml
def cargar_solicitantes():
    ruta = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
    if ruta:
        ruta_absoluta = ruta
        ruta_parcial = ruta.split("/")[-1]
         #PARSEAR EL XML
    tree = ET.parse(ruta)
    #Obtengo el elemento raiz
    root = tree.getroot()

    if root.tag == "solicitantes":
        for solicitante in root:
            id = solicitante.attrib["id"]
            pwd = solicitante.attrib["pwd"]
            nombre = ''
            correo = ''
            telefono = ''
            direccion = ''
            for hijo in solicitante:
                if hijo.tag == "NombreCompleto":
                    nombre = hijo.text
                elif hijo.tag == "CorreoElectronico":
                    correo = hijo.text
                elif hijo.tag == "NumeroTelefono":
                    telefono = hijo.text
                elif hijo.tag == "Direccion":
                    direccion = hijo.text
            nuevo_solicitante = Solicitante(id,pwd,nombre,correo,telefono,direccion)
            listaSolicitantes.insertar(nuevo_solicitante)


        display_area.insert(tk.END, f"Solicitantes cargado: {ruta_parcial}\n")

def cargar_artistas():
    ruta = filedialog.askopenfilename(title="Cargar Archivo", filetypes=(('Text files', '*.xml'), ('All files','*.*')))
    if ruta:
        ruta_absoluta = ruta
        ruta_parcial = ruta.split("/")[-1]
        #PARSEAR EL XML
    tree = ET.parse(ruta)
        #Obtengo el elemento raiz
    root = tree.getroot()

    if root.tag == "Artistas":
            for artista in root:
                id = artista.attrib["id"]
                pwd = artista.attrib["pwd"]
                nombre = ''
                correo = ''
                telefono = ''
                especialidades = ''
                notas = ''
                for hijo in artista:
                    if hijo.tag == "NombreCompleto":
                        nombre = hijo.text
                    elif hijo.tag == "CorreoElectronico":
                        correo = hijo.text
                    elif hijo.tag == "NumeroTelefono":
                        telefono = hijo.text
                    elif hijo.tag == "Especialidades":
                        especialidades = hijo.text
                    elif hijo.tag == "NotasAdicionales":
                        notas = hijo.text
                nuevo_artista = Artista(id,pwd,nombre,correo,telefono,especialidades,notas)
                listaArtistas.insertar(nuevo_artista)
            display_area.insert(tk.END, f"Artistas cargado: {ruta_parcial}\n")   

# Funciones para ver artistas y solicitantes cargados (simulación)
def ver_solicitantes():
       # Usa la instancia global de la lista de solicitantes ya cargada
    global listaSolicitantes

    if listaSolicitantes.primero is None:
        print("La lista de solicitantes está vacía.")
        return

    # Generar la gráfica de la lista
    listaSolicitantes.graficar()  # Llamada correcta al método graficar

    # Crear el área de visualización (display_area)
    display_area = tk.Text(root, height=10, width=50)
    display_area.pack()

    # Insertar el mensaje en el área de visualización
    display_area.insert(tk.END, "Mostrando solicitantes cargados...\n")

    # Ruta del archivo SVG
    #svg_path = "reportes/listaDoble.svg"
    png_path = "reportes/listaDoble.png"

    # Convertir SVG a PNG
    #cairosvg.svg2png(url=svg_path, write_to=png_path)

    # Cargar la imagen PNG
    image = Image.open(png_path)
    photo = ImageTk.PhotoImage(image)

    # Crear un widget Label para mostrar la imagen
    image_label = tk.Label(root, image=photo)
    image_label.pack()
   
    
def ver_artistas():
    global listaArtistas

    if listaArtistas.primero is None:
        print("La lista de solicitantes está vacía.")
        return

    # Generar la gráfica de la lista
    listaArtistas.graficar()  # Llamada correcta al método graficar

    # Crear el área de visualización (display_area)
    display_area = tk.Text(root, height=10, width=50)
    display_area.pack()

    # Insertar el mensaje en el área de visualización
    display_area.insert(tk.END, "Mostrando Artistas cargados...\n")
    png_path = "reportes/listaSimple.png"

    # Cargar la imagen PNG
    image = Image.open(png_path)
    photo = ImageTk.PhotoImage(image)

    # Crear un widget Label para mostrar la imagen
    image_label = tk.Label(root, image=photo)
    image_label.pack()

def Solicitar():
    global id_logueado
    valorSacado = listaSolicitantes.sacardePilaUsuario(id_logueado)
    while valorSacado != None:
        nueva_solicitud = SolicitudCola(valorSacado.id,valorSacado.ruta_xml,id_logueado)
        colaSolicitudes.enqueue(nueva_solicitud)
        valorSacado = listaSolicitantes.sacardePilaUsuario(id_logueado)

def ImagenActual(imagen):
    print(f'Nombre: {imagen.nombre}')
    print(f'Ruta Imagen: {imagen.ruta_imagen}')
    print(f'ID: {imagen.id}')

def CargarXMLFiguras():
    global id_logueado
    ruta = filedialog.askopenfilename(title="Cargar Archivo", filetypes=(('Text files', '*.xml'), ('All files','*.*')))
    #PARSEAR EL XML
    tree = ET.parse(ruta)
    #Obtengo el elemento raiz
    root = tree.getroot()

    id = ''
    if root.tag == "figura":
        for elementos in root:
            if elementos.tag == "nombre":
                id = elementos.attrib["id"]
    
    nueva = SolicitudPila(id,ruta)
    listaSolicitantes.insertaraPilaUsuario(id_logueado,nueva)

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
