# Clase Producto
class Producto:
    def __init__(self, producto_id, nombre, descripcion, precio, stock, categoria):
        self.producto_id = producto_id
        self._nombre = nombre
        self._descripcion = descripcion
        self._precio = precio
        self._stock = stock
        self._categoria = categoria

    # NOMBRE
    @property
    def nombre(self):
        return self._nombre
    @nombre.setter
    def nombre(self, nuevo_nombre):
        self._nombre = nuevo_nombre

    # DESCRIPCION
    @property
    def descripcion(self):
        return self._descripcion
    @descripcion.setter
    def descripcion(self, nueva_descripcion):
        self._descripcion = nueva_descripcion
    
    # PRECIO  
    @property
    def precio(self):
        return self._precio
    @precio.setter
    def precio(self, nuevo_precio):
        self._precio = nuevo_precio
    
    # STOCK
    @property
    def stock(self):
        return self._stock
    @stock.setter
    def stock(self, nuevo_stock):
        self._stock = nuevo_stock

    # CATEGORIA
    @property
    def categoria(self):
        return self._categoria
    @categoria.setter
    def categoria(self, nueva_categoria):
        self._categoria = nueva_categoria

    # OBTENER DETALLES
    def obtener_detalles(self):
        detalles = f"ID: {self.producto_id}\nNombre: {self.nombre}\nDescripción: {self.descripcion}\n"
        detalles += f"Precio: {self.precio}\nStock: {self.stock}\nCategoria: {self.categoria}"
        return detalles
    
    # OBTENER DETALLES PARA STOCK BAJO.................Duda...
    def obtener_detalles_stock(self):
        detalles = f"ID: {self.producto_id}\nNombre: {self.nombre}\nStock: {self.stock}"
        return detalles