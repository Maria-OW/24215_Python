Proyecto Final Integrador - 24215 - Python 2024

Sistema de Gestión de Inventarios

Requisitos: Python 3.x, SQLite y Tkinter

Estructura:
main.py: Inicia la aplicación.
bdd.py: Clase BaseDatos (conexión y consultas a la base de datos SQLite).
inventario.py: Clase "Inventario" (lógica del inventario y operaciones CRUD).
producto.py: Clase "Producto" (definición de las características de los productos que integran el inventario).
interfazinventario.py: Clase "InterfazInventario" (interfaz de usuario utilizando Tkinter).

Al ejecutar el archivo main.py se inicia la aplicación y se muestra una ventana con 2 pestañas (Agregar y Modificar/Eliminar productos).
Para modificar los datos de un producto existente, se lo selecciona con una lista desplegable que trae los datos actuales. Una vez hechas las modificaciones, se guardan los cambios en la base inventario.db creada en bdd.py al cliquear el botón "Modificar Producto". Caso similar para "Eliminar Producto" (elimina el producto seleccionado de la base de datos).
El botón "Mostrar Informe" abre una nueva ventana con el listado de todos los productos del inventario con todos sus detalles.
El botón "Mostrar Stock Bajo" abre una nueva ventana con el listado de todos los productos del inventario que tienen bajo stock y muestra solo Id, nombre, stock y stock mínimo (el cual puede variar según el producto dado que es un valor que carga el usuario).
Se proporciona el botón "Salir" para cerrar la aplicación.
