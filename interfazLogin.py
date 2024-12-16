import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
#Element Tree
import xml.etree.ElementTree as ET
# Importar Tkinter para obtener la ruta de los archivos XML
from tkinter import filedialog, messagebox
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
    global id_logueado
    id_logueado = None
    window.destroy()
    entry_username.delete(0, tk.END)
    entry_password.delete(0, tk.END)
    root.deiconify()

# Función para abrir la ventana del administrador
def open_admin_window():
    
    root.withdraw()
    admin_window = tk.Toplevel(root)
    admin_window.title("Ventana Administrador")
    admin_window.geometry("1100x600")
    admin_window.configure(bg="#2c3e50")

    tk.Label(admin_window, text="Bienvenido Administrador", font=("Helvetica", 16, "bold"), bg="#2c3e50", fg="#ecf0f1").pack(pady=20)

    # Botón de Cerrar Sesión
    tk.Button(admin_window, text="Cerrar Sesión", command=lambda: logout(admin_window), font=("Helvetica", 12), bg="#e74c3c", fg="white", bd=0, cursor="hand2", activebackground="#c0392b", activeforeground="white").place(x=870, y=10)

    # principal
    main_frame = tk.Frame(admin_window, bg="#34495e", bd=5)
    main_frame.place(relx=0.5, rely=0.5, anchor="center", width=970, height=500)

    # Botones 
   
    button_frame = tk.Frame(main_frame, bg="#34495e")
    button_frame.pack(side="left", padx=20, pady=20)

    tk.Button(button_frame, text="Cargar Solicitantes", command=cargar_solicitantes, font=("Helvetica", 12), bg="#1abc9c", fg="white", bd=0, cursor="hand2", activebackground="#16a085", activeforeground="white").pack(pady=10, fill="x")
    tk.Button(button_frame, text="Cargar Artistas", command=cargar_artistas, font=("Helvetica", 12), bg="#1abc9c", fg="white", bd=0, cursor="hand2", activebackground="#16a085", activeforeground="white").pack(pady=10, fill="x")
    tk.Button(button_frame, text="Ver Solicitantes", command=lambda: mostrar_imagen("reportes/listaDoble.png", image_area), font=("Helvetica", 12), bg="#1abc9c", fg="white", bd=0, cursor="hand2", activebackground="#16a085", activeforeground="white").pack(pady=10, fill="x")
    tk.Button(button_frame, text="Ver Artistas", command=lambda: mostrar_imagen("reportes/listaSimple.png", image_area), font=("Helvetica", 12), bg="#1abc9c", fg="white", bd=0, cursor="hand2", activebackground="#16a085", activeforeground="white").pack(pady=10, fill="x")
    tk.Button(button_frame, text="ver Solicitantes en grande", command=ver_solicitantes,font=("Helvetica", 12), bg="#1abc9c", fg="white", bd=0, cursor="hand2", activebackground="#16a085", activeforeground="white").pack(pady=10, fill="x")
    tk.Button(button_frame, text="Ver Artistas en grande", command=ver_artistas,font=("Helvetica", 12), bg="#1abc9c", fg="white", bd=0, cursor="hand2", activebackground="#16a085", activeforeground="white").pack(pady=10, fill="x")
    image_area = tk.Label(main_frame, bg="#ecf0f1", text="Seleccione una opción para mostrar la imagen", font=("Helvetica", 12), anchor="center", relief="sunken")
    image_area.pack(side="right", expand=True, fill="both", padx=20, pady=20)

def mostrar_imagen(ruta, area):
    global id_logueado
    if ruta == "reportes/listaSimple.png" :
        listaArtistas.graficar()
    elif ruta == "reportes/listaDoble.png" :
        listaSolicitantes.graficar() 
    elif ruta == "reportes/cola.png" :
        colaSolicitudes.graficar()
    elif ruta == "reportes/listaCircular.png" :
        artista = listaArtistas.obtenerUsuario(id_logueado)
        artista.procesadas.graficar()
    else:
        messagebox.showerror("Error", "No hay imágenes para mostrar.")

    try:
        img = Image.open(ruta)
        img = img.resize((950, 75), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        area.configure(image=photo, text="")
        area.image = photo
    except Exception as e:
        area.configure(text=f"Error al cargar la imagen: {str(e)}", image="")

# Función para abrir la ventana del artista
def open_artista_window():
    global id_logueado, text_display_area, image_display_area,artista
    artista = listaArtistas.obtenerUsuario(id_logueado)
    root.withdraw()
    artist_window = tk.Toplevel(root)
    artist_window.title("Panel de Artista")
    artist_window.geometry("900x600")
    artist_window.configure(bg="#2c3e50")

    tk.Label(artist_window, text=f"Bienvenido Artista {id_logueado}", 
             font=("Helvetica", 16, "bold"), bg="#2c3e50", fg="#ecf0f1").pack(pady=20)

    tk.Button(artist_window, text="Cerrar Sesión", command=lambda: logout(artist_window), 
              font=("Helvetica", 12), bg="#e74c3c", fg="white", bd=0, cursor="hand2", 
              activebackground="#c0392b", activeforeground="white").place(x=690, y=10)

    frame = tk.Frame(artist_window, bg="#34495e", bd=5)
    frame.place(relx=0.5, rely=0.5, anchor="center", width=825, height=500)

    # Botones
    button_frame = tk.Frame(frame, bg="#34495e")
    button_frame.pack(side="left", padx=20, pady=20)

   
    tk.Button(button_frame, text="Aceptar", command=AceptarSolicitud, 
              font=("Helvetica", 12), bg="#1abc9c", fg="white", bd=0, cursor="hand2", activebackground="#16a085", 
              activeforeground="white").pack(pady=10, fill="x")
    tk.Button(button_frame, text="Ver Cola", command=lambda: mostrar_imagen("reportes/cola.png", image_display_area),
              font=("Helvetica", 12), bg="#1abc9c", fg="white", bd=0, cursor="hand2", 
              activebackground="#16a085", activeforeground="white").pack(pady=10, fill="x")
    tk.Button(button_frame, text="Imágenes Procesadas", 
              command=lambda: mostrar_imagen("reportes/listaCircular.png", image_display_area), 
              font=("Helvetica", 12), bg="#1abc9c", fg="white", bd=0, cursor="hand2", 
              activebackground="#16a085", activeforeground="white").pack(pady=10, fill="x")
    
    tk.Button(button_frame, text="ver Cola en grande", command=colaSolicitudes.graficar,font=("Helvetica", 12), 
              bg="#1abc9c", fg="white", bd=0, cursor="hand2", activebackground="#16a085", activeforeground="white").pack(pady=10, fill="x")
    tk.Button(button_frame, text="Ver Img.Procesadas en grande", command=imagenes_procesadas,font=("Helvetica", 12), 
              bg="#1abc9c", fg="white", bd=0, cursor="hand2", activebackground="#16a085", activeforeground="white").pack(pady=10, fill="x")

    # Área de texto
    text_display_area = tk.Text(frame, width=40, height=10, bg="#ecf0f1", font=("Helvetica", 12), relief="sunken")
    text_display_area.pack(side="top", padx=10, pady=10)

    # Área de imagen
    image_display_area = tk.Label(frame, bg="#ecf0f1", text="Seleccione una opción para mostrar la imagen", font=("Helvetica", 12), anchor="center", relief="sunken")
    image_display_area.pack(side="left", expand=True, fill="both", padx=10, pady=10)

    actualizar_text_display_area()

def actualizar_text_display_area():
    """Actualiza el área de texto con la información del primer elemento en la cola."""
    text_display_area.delete(1.0, tk.END)
    if colaSolicitudes.verPrimero() is None:
        text_display_area.insert(tk.END, "No hay solicitudes")
    else:
        solicitud = colaSolicitudes.verPrimero()
        text_display_area.insert(tk.END, f"SOLICITUD ID: {solicitud.id}\n")
        text_display_area.insert(tk.END, f"Ruta XML: {solicitud.ruta_xml}\n")
        text_display_area.insert(tk.END, f"Solicitante: {solicitud.id_solicitante}")  

def imagenes_procesadas():
    artista = listaArtistas.obtenerUsuario(id_logueado)
    artista.procesadas.graficar()
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
    actualizar_text_display_area()

# Función para abrir la ventana del solicitante
def open_solicitante_window():
    global id_logueado, applicant_image_display_area
    root.withdraw()

    # Crear ventana del solicitante
    applicant_window = tk.Toplevel(root)
    applicant_window.title("Ventana Solicitante")
    applicant_window.geometry("800x600")
    applicant_window.configure(bg="#1e272e")  # Fondo oscuro para resaltar los colores

    solicitante = listaSolicitantes.buscar(id_logueado)

    # Etiqueta de bienvenida
    tk.Label(
        applicant_window,
        text=f"Bienvenido Solicitante {id_logueado}",
        font=("Helvetica", 16, "bold"),
        bg="#1e272e",
        fg="#f5f6fa"
    ).pack(pady=20)

    # Botón de cerrar sesión
    tk.Button(
        applicant_window,
        text="Cerrar Sesión",
        command=lambda: logout(applicant_window),
        font=("Helvetica", 12),
        bg="#e74c3c",
        fg="white",
        bd=0,
        cursor="hand2",
        activebackground="#c0392b",
        activeforeground="white"
    ).place(x=670, y=10)

    # Frame para botones y áreas de visualización
    frame = tk.Frame(applicant_window, bg="#34495e", bd=5, relief="ridge")
    frame.place(relx=0.5, rely=0.5, anchor="center", width=750, height=450)

    # Botones del menú
    button_frame = tk.Frame(frame, bg="#34495e")
    button_frame.pack(side="left", padx=20, pady=20)

    tk.Button(
        button_frame, text="Solicitar", command=Solicitar,
        font=("Helvetica", 12), bg="#00cec9", fg="white", bd=0,
        cursor="hand2", activebackground="#00b894", activeforeground="white"
    ).pack(pady=10, fill="x")

    tk.Button(
        button_frame, text="Ver Galería", command=open_gallery_window,
        font=("Helvetica", 12), bg="#00cec9", fg="white", bd=0,
        cursor="hand2", activebackground="#00b894", activeforeground="white"
    ).pack(pady=10, fill="x")

    tk.Button(
        button_frame, text="Cargar Figura", command=CargarXMLFiguras,
        font=("Helvetica", 12), bg="#00cec9", fg="white", bd=0,
        cursor="hand2", activebackground="#00b894", activeforeground="white"
    ).pack(pady=10, fill="x")

    tk.Button(
        button_frame, text="Ver Pila", command=ver_pila,
        font=("Helvetica", 12), bg="#00cec9", fg="white", bd=0,
        cursor="hand2", activebackground="#00b894", activeforeground="white"
    ).pack(pady=10, fill="x")

    tk.Button(
        button_frame, text="Ver Lista", command=ver_lista,
        font=("Helvetica", 12), bg="#00cec9", fg="white", bd=0,
        cursor="hand2", activebackground="#00b894", activeforeground="white"
    ).pack(pady=10, fill="x")

    # Espacio para mostrar imágenes
    applicant_image_display_area = tk.Label(
        frame, bg="#f5f6fa", text="No hay imagen seleccionada",
        font=("Helvetica", 12), relief="sunken"
    )
    applicant_image_display_area.pack(side="right", expand=True, fill="both", padx=10, pady=10)

# Función para abrir la ventana de galería
def open_gallery_window():
    global id_logueado, gallery_image_display_area, imagen_actual, solicitante

    # Buscar solicitante
    solicitante = listaSolicitantes.buscar(id_logueado)
    if not solicitante or len(solicitante.imagenes) == 0:
        messagebox.showerror("Error", "No hay imágenes para mostrar.")
        return

    # Inicializar la primera imagen
    imagen_actual = solicitante.imagenes.primero.valor

    # Crear ventana principal de galería
    gallery_window = tk.Toplevel(root)
    gallery_window.title("Galería")
    gallery_window.geometry("900x600")
    gallery_window.configure(bg="#2c3e50")

    tk.Label(gallery_window, text="Galería de Imágenes", font=("Helvetica", 20, "bold"), bg="#2c3e50", fg="#ecf0f1").pack(pady=20)


    # Frame para botones y visualización
    frame = tk.Frame(gallery_window, bg="#34495e", bd=5)
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    gallery_image_display_area = tk.Label(frame, text="Cargando imagen...", bg="#34495e", fg="#ecf0f1", font=("Helvetica", 14))
    gallery_image_display_area.pack(expand=True)

    # Frame para los botones
    button_frame = tk.Frame(gallery_window, bg="#2c3e50")
    button_frame.pack(pady=10)

    # Botón Anterior
    tk.Button(button_frame, text="Anterior", command=ver_anterior, font=("Helvetica", 12, "bold"), bg="#1abc9c", fg="white", bd=0, cursor="hand2", activebackground="#16a085", activeforeground="white").grid(row=0, column=0, padx=10)

    # Botón Siguiente
    tk.Button(button_frame, text="Siguiente", command=ver_siguiente, font=("Helvetica", 12, "bold"), bg="#1abc9c", fg="white", bd=0, cursor="hand2", activebackground="#16a085", activeforeground="white").grid(row=0, column=1, padx=10)

    # Botón Cerrar
    tk.Button(button_frame, text="Cerrar", command=gallery_window.destroy, font=("Helvetica", 12, "bold"), bg="#e74c3c", fg="white", bd=0, cursor="hand2", activebackground="#c0392b", activeforeground="white").grid(row=0, column=2, padx=10)

    # Cargar la imagen inicial
    cargar_imagen(imagen_actual)

# Función para cargar imágenes
def cargar_imagen(imagen):
    global gallery_image_display_area
    try:
        img = Image.open(imagen.ruta_imagen)
        img = img.resize((300, 300), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        gallery_image_display_area.configure(image=img_tk, text="")
        gallery_image_display_area.image = img_tk  # Evita que la imagen sea eliminada por el recolector de basura
    except Exception as e:
        gallery_image_display_area.configure(text=f"Error al cargar imagen:\n{e}")

# Función para ver la imagen anterior
def ver_anterior():
    global imagen_actual
    imagen_actual = solicitante.imagenes.obtenerAnterior(imagen_actual.id)
    cargar_imagen(imagen_actual)

# Función para ver la imagen siguiente
def ver_siguiente():
    global imagen_actual
    imagen_actual = solicitante.imagenes.obtenerSiguiente(imagen_actual.id)
    cargar_imagen(imagen_actual)
# Función para ver pila
def ver_pila():

    solicitante:Solicitante = listaSolicitantes.buscar(id_logueado)
    if solicitante.pila.isEmpty():
        messagebox.showinfo("Pila", "La pila está vacía")
    else:    
        solicitante.pila.graficar()

# Función para ver lista
def ver_lista():

    global id_logueado
   
    solicitante:Solicitante = listaSolicitantes.buscar(id_logueado)
    print(len(solicitante.imagenes))
    
    solicitante.imagenes.graficar()

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


        #display_area.insert(tk.END, f"Solicitantes cargado: {ruta_parcial}\n")

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
            #display_area.insert(tk.END, f"Artistas cargado: {ruta_parcial}\n")   

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
    #display_area = tk.Text(root, height=10, width=50)
    #display_area.pack()

    # Insertar el mensaje en el área de visualización
    #display_area.insert(tk.END, "Mostrando solicitantes cargados...\n")

    # Ruta del archivo SVG
    #svg_path = "reportes/listaDoble.svg"
    png_path = "reportes/listaDoble.png"

    # Convertir SVG a PNG
    #cairosvg.svg2png(url=svg_path, write_to=png_path)

    # Cargar la imagen PNG
    image = Image.open(png_path)
    photo = ImageTk.PhotoImage(image)

    # Crear un widget Label para mostrar la imagen
    #image_label = tk.Label(root, image=photo)
    #image_label.pack()   

def ver_artistas():
    global listaArtistas

    if listaArtistas.primero is None:
        print("La lista de solicitantes está vacía.")
        return

    # Generar la gráfica de la lista
    listaArtistas.graficar()  # Llamada correcta al método graficar

    # Crear el área de visualización (display_area)
    #display_area = tk.Text(root, height=10, width=50)
    #display_area.pack()

    # Insertar el mensaje en el área de visualización
    #display_area.insert(tk.END, "Mostrando Artistas cargados...\n")
    png_path = "reportes/listaSimple.png"

    # Cargar la imagen PNG
    image = Image.open(png_path)
    photo = ImageTk.PhotoImage(image)

    # Crear un widget Label para mostrar la imagen
    #image_label = tk.Label(root, image=photo)
    #image_label.pack()

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
root.title("IPCART-STUDIO")
root.geometry("600x400")

root.resizable(False, False)
root.configure(bg="#2c3e50")

# Marco para centrar y decorar el formulario
frame = tk.Frame(root, bg="#34495e", bd=5) 
frame.place(relx=0.5, rely=0.5, anchor="c", width=350, height=300)

# Título del formulario
tk.Label(frame, text="Bienvenido", font=("Helvetica", 16, "bold"), bg="#34495e", fg="#ecf0f1").pack(pady=10)

# Entrada de usuario
tk.Label(frame, text="Usuario", font=("Helvetica", 12), bg="#34495e", fg="#ecf0f1").pack(pady=5)
entry_username = tk.Entry(frame, font=("Helvetica", 12))
entry_username.pack(pady=5, ipady=5, ipadx=5, fill="x")

# Entrada de contraseña
tk.Label(frame, text="Contraseña", font=("Helvetica", 12), bg="#34495e", fg="#ecf0f1").pack(pady=5)
entry_password = tk.Entry(frame, show="*", font=("Helvetica", 12))
entry_password.pack(pady=5, ipady=5, ipadx=5, fill="x")

# Botón de login
tk.Button(frame, text="INGRESAR", command=login, font=("Helvetica", 12, "bold"), bg="#1abc9c", fg="white", bd=0, cursor="hand2", activebackground="#16a085", activeforeground="white").pack(pady=20, fill="x")


root.mainloop()
