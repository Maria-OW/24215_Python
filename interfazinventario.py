import tkinter as tk
from tkinter import ttk, messagebox 
import time
from bdd import BaseDatos  
from inventario import Inventario 
from producto import Producto  


class InterfazInventario:
    def __init__(self, root):
        # Inicialización de la clase BaseDatos para manejar la base de datos
        self.base_datos = BaseDatos()
        # Inicialización de la clase Inventario para manejar el inventario de productos
        self.inventario = Inventario()
        # Carga de los productos desde la base de datos al inventario
        self.cargar_productos_desde_db()
        self.cargar_bajo_stock_desde_db()
        

        # Configuración de la ventana principal de la aplicación
        self.root = root
        self.root.title("Sistema de Gestión de Inventario")
        self.root.geometry("800x600")

        style = ttk.Style()
        style.configure('TNotebook.Tab', font=('Helvetica', '11', 'bold'))

        # Configuración para mostrar pestañas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both')

        # Creación de las pestañas "Agregar Producto" y "Modificar Producto" 
        self.pagina_agregar = ttk.Frame(self.notebook)
        self.pagina_modificar = ttk.Frame(self.notebook)           
        self.notebook.add(self.pagina_agregar, text='Agregar Producto')
        self.notebook.add(self.pagina_modificar, text='Modificar o Eliminar Producto')

        # Creación de la interfaz para agregar un nuevo producto
        self.crear_interfaz_agregar_producto()
        # Creación de la interfaz para modificar un producto existente
        self.crear_interfaz_modificar_producto()
        # Creación del botón para eliminar un producto
        self.crear_boton_eliminar_producto() 
        # Creación del botón para mostrar el listado de productos
        self.crear_boton_mostrar_listado()
        # Creación del botón de bajo stock
        self.crear_boton_mostrar_stockbajo()
        # Creación del boton cerrar
        self.crear_boton_cerrar_aplicacion()
        
    #Carga de los productos desde la base de datos al inventario (conexión con bdd para la consulta)
    def cargar_productos_desde_db(self):
        productos_db = self.base_datos.obtener_productos()
        self.inventario.productos = productos_db
        
    def cargar_bajo_stock_desde_db(self):
        productos_db = self.base_datos.buscar_stock_bajo()
        self.inventario.productos = productos_db

    # Interfaz para agregar un nuevo producto
    def crear_interfaz_agregar_producto(self):
        etiquetas_agregar = ["Nombre del Producto", "Descripción", "Precio", "Stock", "Categoría"]
        self.entries_agregar = {}
        for i, etiqueta in enumerate(etiquetas_agregar):
            tk.Label(self.pagina_agregar, text=etiqueta, font=("Arial", 12)).grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(self.pagina_agregar, font=("Arial", 12))
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries_agregar[etiqueta] = entry
        self.boton_agregar = tk.Button(self.pagina_agregar, text="Agregar Producto", command=self.agregar_producto, font=("Arial", 12), bg="#4CAF50", fg="white")
        self.boton_agregar.grid(row=len(etiquetas_agregar) + 1, column=0, columnspan=2, pady=10)

    # Interfaz para modificar un producto existente
    def crear_interfaz_modificar_producto(self):
        etiquetas_modificar = ["Seleccione Producto:", "Nombre del Producto", "Descripción", "Precio", "Stock", "Categoría"]
        self.combo_modificar = ttk.Combobox(self.pagina_modificar, values=["Seleccionar"] + [producto.nombre for producto in self.inventario.productos], font=("Arial", 12))
        self.combo_modificar.grid(row=0, column=1, padx=10, pady=5)
        self.combo_modificar.set("Seleccionar")
        self.combo_modificar.bind("<<ComboboxSelected>>", self.actualizar_datos_producto_seleccionado)  
        self.entries_modificar = {}
        for i, etiqueta in enumerate(etiquetas_modificar[1:]):
            tk.Label(self.pagina_modificar, text=etiqueta, font=("Arial", 12)).grid(row=i + 1, column=0, padx=10, pady=5)
            entry = tk.Entry(self.pagina_modificar, font=("Arial", 12))
            entry.grid(row=i + 1, column=1, padx=10, pady=5)
            self.entries_modificar[etiqueta] = entry
        self.boton_modificar = tk.Button(self.pagina_modificar, text="Modificar Producto", command=self.modificar_producto, font=("Arial", 12), bg="#008CBA", fg="white")  #modificar_producto
        self.boton_modificar.grid(row=len(etiquetas_modificar) + 1, column=0, columnspan=2, pady=10)


    # Botón para eliminar productos
    def crear_boton_eliminar_producto(self):
        self.boton_eliminar = tk.Button(self.pagina_modificar, text="Eliminar Producto", command=self.eliminar_producto, font=("Arial", 12), bg="#FF5733", fg="white")
        self.boton_eliminar.grid(row=8, column=0, columnspan=2, pady=10)

    # Botón para mostrar el listado completo del inventario
    def crear_boton_mostrar_listado(self):
        self.boton_mostrar_listado = tk.Button(self.root, text="Mostrar Listado", command=self.mostrar_listado, font=("Arial", 12), bg="#333", fg="white")
        self.boton_mostrar_listado.pack(pady=10)
    
    # Botón para mostrar listdo de productos con bajo stock    
    def crear_boton_mostrar_stockbajo(self):
        self.boton_mostrar_stockbajo = tk.Button(self.root, text="Mostrar Stock bajo", command=self.mostrar_stockbajo, font=("Arial", 12), bg="#333", fg="white")
        self.boton_mostrar_stockbajo.pack(pady=10)
        
    # Botón para cerrar aplicacion
    def crear_boton_cerrar_aplicacion(self):
        self.boton_cerrar_aplicacion = tk.Button(self.root, text="Salir", command=self.cerrar_aplicacion, font=("Arial", 12, "bold"), bg="#fff", fg="red")
        self.boton_cerrar_aplicacion.pack(pady=10)
        


###### FUNCIONES ######

    #Agrega un producto nuevo
    def agregar_producto(self):
        try:
            nombre = self.entries_agregar["Nombre del Producto"].get()
            descripcion = self.entries_agregar["Descripción"].get()
            precio = float(self.entries_agregar["Precio"].get())
            stock = int(self.entries_agregar["Stock"].get())
            categoria = self.entries_agregar["Categoría"].get()
            producto = Producto(len(self.inventario.productos) + 1, nombre, descripcion, precio, stock, categoria)
            self.inventario.agregar_producto(producto)
            self.base_datos.agregar_producto(producto)
            self.combo_modificar["values"] = ["Seleccionar"] + [p.nombre for p in self.inventario.productos]
            messagebox.showinfo("Éxito", "Producto agregado correctamente.")
        except ValueError:
            messagebox.showerror("Error", "Ingrese datos válidos para el producto.")

    #Devuelve datos del producto seleccioando en el combo
    def actualizar_datos_producto_seleccionado(self, event):
        selected_product = self.combo_modificar.get()
        if selected_product != "Seleccionar":
            producto = next((p for p in self.inventario.productos if p.nombre == selected_product), None)
            if producto:
                self.entries_modificar["Nombre del Producto"].delete(0, tk.END)
                self.entries_modificar["Nombre del Producto"].insert(0, producto.nombre)
                self.entries_modificar["Descripción"].delete(0, tk.END)
                self.entries_modificar["Descripción"].insert(0, producto.descripcion)
                self.entries_modificar["Precio"].delete(0, tk.END)
                self.entries_modificar["Precio"].insert(0, str(producto.precio))
                self.entries_modificar["Stock"].delete(0, tk.END)
                self.entries_modificar["Stock"].insert(0, str(producto.stock)) 
                self.entries_modificar["Categoría"].delete(0, tk.END)
                self.entries_modificar["Categoría"].insert(0, producto.categoria)
    
    #Modifica en la base los datos del producto seleccionado en el combo
    def modificar_producto(self):
        selected_product = self.combo_modificar.get()
        if selected_product != "Seleccionar":
            producto = next((p for p in self.inventario.productos if p.nombre == selected_product), None)
            if producto:
                nueva_descripcion = self.entries_modificar["Descripción"].get()
                nuevo_precio = self.entries_modificar["Precio"].get()
                nuevo_stock = self.entries_modificar["Stock"].get()
                nuevo_categoria = self.entries_modificar["Categoría"].get()
                if nuevo_precio and nuevo_stock and nuevo_categoria and nueva_descripcion:
                    try:
                        nuevo_precio = float(nuevo_precio)
                        nuevo_stock = int(nuevo_stock)
                        producto.descripcion = nueva_descripcion
                        producto.precio = nuevo_precio
                        producto.stock = nuevo_stock
                        producto.categoria = nuevo_categoria                        
                        self.base_datos.actualizar_producto(producto)
                        self.base_datos.cerrar_conexion()
                        self.base_datos = BaseDatos()
                        messagebox.showinfo("Éxito", "Producto modificado correctamente.")
                    except ValueError:
                        messagebox.showerror("Error", "Ingrese datos válidos para precio y stock.")
                else:
                    messagebox.showerror("Error", "Ingrese nuevo precio, stock, categoría y descripción.")
            else:
                messagebox.showerror("Error", "Producto no encontrado.")
        else:
            messagebox.showerror("Error", "Seleccione un producto para modificar.")

    #Elimina el producto seleccionado en el combo
    def eliminar_producto(self):
        selected_product = self.combo_modificar.get()
        if selected_product != "Seleccionar":
            producto = next((p for p in self.inventario.productos if p.nombre == selected_product), None)
            if producto:
                self.inventario.eliminar_producto(producto)
                self.base_datos.eliminar_producto(producto)
                self.combo_modificar["values"] = ["Seleccionar"] + [p.nombre for p in self.inventario.productos]
                messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
            else:
                messagebox.showerror("Error", "Producto no encontrado.")
        else:
            messagebox.showerror("Error", "Seleccione un producto para eliminar.")

    #Muestra el listado completo del inventario
    def mostrar_listado(self):
        listado = self.inventario.generar_listado()
        mensaje = "\n\n".join(listado)

        # Crear una ventana secundaria para mostrar el listado
        ventana_listado = tk.Toplevel(self.root)
        ventana_listado.title("Listado de Productos")
        
        # Crear un frame para contener el mensaje con desplazamiento
        frame_mensaje = tk.Frame(ventana_listado)
        frame_mensaje.pack(fill="both", expand=True)

        # Crear un scrollbar para desplazarse verticalmente
        scrollbar = ttk.Scrollbar(frame_mensaje, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        # Crear un Text widget para mostrar el mensaje
        txt_listado = tk.Text(frame_mensaje, yscrollcommand=scrollbar.set)
        txt_listado.pack(fill="both", expand=True)
        txt_listado.insert("1.0", mensaje)

        # Configurar el scrollbar para controlar el desplazamiento del Text widget
        scrollbar.config(command=txt_listado.yview)
    
    
    
    #Muestra (o no!!!) el listado de productos con stock bajo
    def mostrar_stockbajo(self):                                    # No filtra por < 5!!! 
        #messagebox.showinfo("Bajo Stock", "bajo")

        listado = self.inventario.generar_stock_bajo()
        mensaje = "\n\n".join(listado)
        
        ventana_listado = tk.Toplevel(self.root)
        ventana_listado.title("Listado de productos con bajo stock")
        
        frame_mensaje = tk.Frame(ventana_listado)
        frame_mensaje.pack(fill="both", expand=True)
        
        # Crear un scrollbar para desplazarse verticalmente
        scrollbar = ttk.Scrollbar(frame_mensaje, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        # Crear un Text widget para mostrar el mensaje
        txt_listado = tk.Text(frame_mensaje, yscrollcommand=scrollbar.set)
        txt_listado.pack(fill="both", expand=True)
        txt_listado.insert("1.0", mensaje)

        # Configurar el scrollbar para controlar el desplazamiento del Text widget
        scrollbar.config(command=txt_listado.yview)
        
        
    #Cierra la aplicación
    def cerrar_aplicacion(self):
        self.root.destroy()


