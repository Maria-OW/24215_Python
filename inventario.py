# Clase Inventario
class Inventario:
    def __init__(self):
        self.productos = []
        self.productos_bajo_stock = []

    def agregar_producto(self, producto):
        self.productos.append(producto)

    def eliminar_producto(self, producto):
        self.productos = [p for p in self.productos if p.producto_id != producto.producto_id]


    def buscar_producto(self, producto_id):
        for producto in self.productos:
            if producto.producto_id == producto_id:
                return producto
        return None

    def generar_listado(self):
        listado = [producto.obtener_detalles() for producto in self.productos]
        return listado
    
    def generar_stock_bajo(self):                                                          #Duda...
        stock_bajo = [producto.obtener_detalles_stock() for producto in self.productos_bajo_stock]
        return stock_bajo
