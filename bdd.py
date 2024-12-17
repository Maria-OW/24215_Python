import sqlite3
from tkinter import ttk, messagebox 
from producto import Producto  # Importar la clase Producto del módulo producto.py

# Clase para manejar la base de datos
class BaseDatos:
    def __init__(self):
        # Conexión a la base de datos SQLite
        self.conexion = sqlite3.connect("inventario.db")
        self.cursor = self.conexion.cursor()  # Creación de un cursor para ejecutar consultas SQL
        self.crear_tabla()  # Llamada al método para crear la tabla si no existe

    def crear_tabla(self):
        # Ejecución de la consulta SQL para crear la tabla de productos si no existe
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                producto_id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                precio REAL NOT NULL,
                stock INTEGER NOT NULL,                
                categoria TEXT
            )
        ''')
        self.conexion.commit()  # Confirmación de los cambios en la base de datos

    def obtener_productos(self):
        # Ejecución de la consulta SQL para obtener el listado de productos
        self.cursor.execute("SELECT * FROM productos")
        filas = self.cursor.fetchall()  # Obtención de todas las filas resultantes
        return [Producto(*fila) for fila in filas] # Creación de objetos Producto a partir de las filas y retorno de una lista de productos

    def agregar_producto(self, producto):
        # Ejecución de la consulta SQL para insertar un nuevo producto en la tabla
        self.cursor.execute('''
            INSERT INTO productos (nombre, descripcion, precio, stock, categoria)
            VALUES (?, ?, ?, ?, ?)
        ''', (producto.nombre, producto.descripcion, producto.precio, producto.stock, producto.categoria))
        self.conexion.commit()  # Confirmación de los cambios en la base de datos

    def eliminar_producto(self, producto):
        # Ejecución de la consulta SQL para borrar un producto de la tabla
        self.cursor.execute('''
             DELETE FROM productos WHERE producto_id=?               
        ''', (producto.producto_id,))
        self.conexion.commit()
        
    def actualizar_producto(self, producto):
        try:
            # Ejecución de la consulta SQL para actualizar el producto
            self.cursor.execute('''
                UPDATE productos SET nombre=?, descripcion=?, precio=?, stock=?, categoria=? WHERE producto_id=?
            ''', (producto.nombre, producto.descripcion, producto.precio, producto.stock, producto.categoria, producto.producto_id))  
            self.conexion.commit()  # Confirmar los cambios en la base de datos
        except sqlite3.Error as error:
            # Manejar cualquier error de base de datos
            messagebox.showerror("Error en base de datos", f"No se pudo actualizar el producto: {error}")

           
    def buscar_stock_bajo(self, producto):
        # Ejecución de la consulta SQL para obtener el listado de productos con stock bajo
            self.cursor.execute('''SELECT id_producto, nombre, stock FROM productos WHERE tock < 5''')
            productos_bajos=self.cursor.fetchall()       

            if productos_bajos:
                    mensaje = "Productos con stock bajo:\n"
                    for producto in productos_bajos:
                        mensaje += f"ID: {producto[0]}, Nombre: {producto[1]}, Stock: {producto[4]}\n"
                    messagebox.showwarning("Stock Bajo", mensaje)
            else:
                    messagebox.showinfo("Stock", "No hay productos con stock bajo.")


        
    
    def buscar_productos_por_nombre(self, nombre):
        try:
            # Consulta SQL para buscar productos por coincidencia de nombre
            self.cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", ('%' + nombre + '%',))
            productos = self.cursor.fetchall()
            self.conexion.commit()
        except sqlite3.Error as error:
            # Manejar cualquier error de base de datos
            messagebox.showerror("Error en base de datos", f"No se pudo obtener el producto: {error}")
        return productos
    
    
    def cerrar_conexion(self):
        self.conexion.close()  # Cierre de la conexión a la base de datos
        
    

  
