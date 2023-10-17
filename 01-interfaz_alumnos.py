from tkinter import *
from tkinter import messagebox

raiz = Tk()
nombre = "Mynor Morales"

# ---------------------- Funciones ----------------------

# Función para cargar datos desde el archivo


def cargar_datos_desde_archivo():
    codificaciones = ["utf-8", "latin-1", "cp1252"]

    for codificacion in codificaciones:
        try:
            cursos = []
            with open("cursos_inscritos.txt", "r", encoding=codificacion) as archivo:
                lines = archivo.readlines()
                curso = {}
                for line in lines:
                    line = line.strip()
                    if line.startswith("Curso: "):
                        if curso:
                            cursos.append(curso)
                        curso = {}
                        curso["nombre"] = line.replace("Curso: ", "")
                    elif line.startswith("Código: "):
                        curso["codigo"] = line.replace("Código: ", "")
                    elif line.startswith("Horario: "):
                        curso["horario"] = line.replace("Horario: ", "")
                if curso:
                    cursos.append(curso)
            return cursos
        except UnicodeDecodeError:
            continue

    # Si ninguna codificación funcionó, tira error
    return []


# Cargar datos desde el archivo
datos_cursos = cargar_datos_desde_archivo()

# Función para mostrar notas y habilitar la descarga de certificado


def mostrar_notas_curso(curso):
    for curso_info in datos_cursos:
        if curso_info["nombre"] == curso:
            # Aquí se asume que la nota es 65
            nota = 65

            nota_label = Label(aFrame, text=f"Nota del curso: {nota}")
            nota_label.grid(row=3, column=0, columnspan=4)

            if nota > 61:
                descargar_button = Button(aFrame, text="Descargar Certificado", cursor="hand2",
                                          command=lambda codigo=curso_info["codigo"]: descargar_certificado(codigo))
                descargar_button.grid(row=4, column=0, columnspan=4)
            break

# Función para descargar el certificado


def descargar_certificado(codigo_curso):
    # Generar el contenido del certificado
    certificado_contenido = f"Certificado para el curso con código {codigo_curso}. ¡Felicitaciones!\n"
    certificado_contenido += "Este es un certificado de ejemplo."

    # Guardar el certificado en un archivo .txt
    with open(f"certificado_{codigo_curso}.txt", "w", encoding="utf-8") as certificado_file:
        certificado_file.write(certificado_contenido)

    messagebox.showinfo("Certificado Descargado",
                        f"Certificado para el curso {codigo_curso} descargado con éxito. Puedes encontrarlo en el archivo certificado_{codigo_curso}.txt")


def crear_botones_cursos_inscritos():
    for i in range(len(datos_cursos)):
        nombre = datos_cursos[i]["nombre"]
        curso_info = f"Curso: {nombre}"
        # Calcule la fila y la columna para el botón
        fila = i // 4
        columna = i % 4
        button = Button(aFrame, text=curso_info, cursor="hand2",
                        command=lambda curso=nombre: mostrar_notas_curso(curso))
        button.grid(row=2+fila, column=columna, padx=10, pady=10)


def mostrar_ventana_asignacion():
    ventana_asignacion = Toplevel(raiz)
    ventana_asignacion.title("Asignación de Cursos")

    aFrame = Frame(ventana_asignacion, bg="gray")
    aFrame.pack(fill=BOTH, expand=True)

    numero_cursos = 10
    nombres_cursos = ["Curso 1", "Curso 2", "Curso 3", "Curso 4", "Curso 5",
                      "Curso 6", "Curso 7", "Curso 8", "Curso 9", "Curso 10"]
    codigos_cursos = ["001", "002", "003", "004",
                      "005", "006", "007", "008", "009", "010"]
    horarios_cursos = ["Lunes 9:00 AM", "Martes 2:00 PM", "Miércoles 11:30 AM", "Jueves 4:00 PM",
                       "Viernes 10:00 AM", "Sábado 1:30 PM", "Domingo 3:45 PM", "Lunes 9:00 AM",
                       "Martes 2:00 PM", "Miércoles 11:30 AM"]

    cursos_seleccionados = []

    def agregar_curso_seleccionado(curso_info):
        cursos_seleccionados.append(curso_info)
        lista_cursos_seleccionados.insert(END, curso_info)

    def quitar_curso_seleccionado():
        seleccion = lista_cursos_seleccionados.curselection()
        if seleccion:
            indice = seleccion[0]
            lista_cursos_seleccionados.delete(indice)
            del cursos_seleccionados[indice[0]]

    def asignar_cursos():
        # Guardar los cursos en un archivo de texto
        with open("cursos_inscritos.txt", "w") as file:
            for curso in cursos_seleccionados:
                file.write(curso + "\n")
        messagebox.showinfo("Asignación de Cursos",
                            "Cursos asignados y guardados en 'cursos_inscritos.txt'")

    def crear_botones_cursos(numero_cursos, nombres_cursos, codigos_cursos, horarios_cursos):
        # Leer los cursos asignados desde el archivo
        try:
            with open("cursos_inscritos.txt", "r") as file:
                cursos_asignados = [line.strip() for line in file]
        except FileNotFoundError:
            cursos_asignados = []

        for i in range(numero_cursos):
            nombre = nombres_cursos[i]
            codigo = codigos_cursos[i]
            horario = horarios_cursos[i]
            curso_info = f"Curso: {nombre}\nCódigo: {codigo}\nHorario: {horario}"
            fila = i // 4
            columna = i % 4
            button = Button(aFrame, text=curso_info, cursor="hand2")

            # Deshabilitar el botón si el curso ya está asignado
            if curso_info in cursos_asignados:
                button.config(state=DISABLED)

            button.grid(row=2 + fila, column=columna, padx=10, pady=10)
            # Configurar la acción al hacer clic en el botón
            button.config(
                command=lambda curso_info=curso_info: agregar_curso_seleccionado(curso_info))

    crear_botones_cursos(numero_cursos, nombres_cursos,
                         codigos_cursos, horarios_cursos)

    lista_cursos_seleccionados = Listbox(aFrame)
    lista_cursos_seleccionados.grid(
        row=3 + numero_cursos // 4, columnspan=4, padx=10, pady=10)

    boton_quitar = Button(aFrame, text="Quitar Curso",
                          cursor="hand2", command=quitar_curso_seleccionado)
    boton_quitar.grid(row=4 + numero_cursos // 4,
                      columnspan=4, padx=10, pady=10)

    boton_asignar = Button(aFrame, text="Asignar Cursos",
                           cursor="hand2", command=asignar_cursos)
    boton_asignar.grid(row=5 + numero_cursos // 4,
                       columnspan=4, padx=10, pady=10)

    # Botón para cerrar la ventana de asignación de cursos
    boton_cerrar = Button(aFrame, text="Cerrar",
                          cursor="hand2", command=ventana_asignacion.destroy)
    boton_cerrar.grid(row=6 + numero_cursos // 4,
                      columnspan=4, padx=10, pady=10)


def mostrar_ventana_desasignacion():
    ventana_desasignacion = Toplevel(raiz)
    ventana_desasignacion.title("Desasignación de Cursos")

    aFrameDesasignacion = Frame(ventana_desasignacion, bg="gray")
    aFrameDesasignacion.pack(fill=BOTH, expand=True)

    # Cargar los cursos inscritos desde el archivo
    try:
        with open("cursos_inscritos.txt", "r") as file:
            cursos_desasignados = [line.strip() for line in file]
    except FileNotFoundError:
        cursos_desasignados = []

    # Crear la lista de cursos inscritos
    lista_cursos_desasignados = Listbox(aFrameDesasignacion)
    lista_cursos_desasignados.grid(
        row=0, columnspan=4, padx=10, pady=10)

    # Llenar la lista de cursos inscritos
    for curso in cursos_desasignados:
        lista_cursos_desasignados.insert(END, curso)

    # Función para desasignar un curso
    def desasignar_curso():
        seleccion = lista_cursos_desasignados.curselection()
        if seleccion:
            indice = seleccion[0]
            curso_desasignado = cursos_desasignados[indice]
            lista_cursos_desasignados.delete(indice)
            cursos_desasignados.remove(curso_desasignado)
            # Actualizar el archivo de cursos inscritos
            with open("cursos_inscritos.txt", "w") as file:
                for curso in cursos_desasignados:
                    file.write(curso + "\n")
            messagebox.showinfo("Desasignación de Cursos",
                                f"Curso desasignado: {curso_desasignado}")

    boton_desasignar = Button(aFrameDesasignacion, text="Desasignar Curso",
                              cursor="hand2", command=desasignar_curso)
    boton_desasignar.grid(row=1, columnspan=4, padx=10, pady=10)

# -------------------------------- Vista gráfica --------------------------------


raiz.title("Hogwarts")
aFrame = Frame(raiz, bg="gray")
aFrame.pack(fill=BOTH, expand=True)

saludo = Label(
    aFrame, text=f"Bienvenido {nombre}", bg="gray", font=("Helvetica", 16))
saludo.grid(row=1, column=0, padx=10, pady=10, columnspan=4)

crear_botones_cursos_inscritos()

botonAsign = Button(aFrame, text="Asignación de Cursos",
                    cursor="hand2", command=mostrar_ventana_asignacion)
botonAsign.grid(row=(len(datos_cursos) // 4) + 3, column=0, padx=10, pady=10)

botonDesasign = Button(aFrame, text="Desasignación de Cursos",
                       cursor="hand2", command=mostrar_ventana_desasignacion)
botonDesasign.grid(row=(len(datos_cursos) // 4) + 3, column=3)

raiz.mainloop()
