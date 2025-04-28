import pymysql
import pymysql.cursors
import config  # Archivo de configuración para credenciales de la base de datos
from colorama import Fore, init
init(autoreset=True)

class Database:
    """
    Clase para manejar la conexión a la base de datos.
    """
    def __enter__(self):
        try:
            # Inicializa la conexión a la base de datos
            self.conn = pymysql.connect(**config.DB_CONFIG)
            self.cur = self.conn.cursor(pymysql.cursors.DictCursor)
            return self.cur
        except Exception as e:
            print(Fore.RED + f"Error de conexión: {e}")
            self.conn = None
            self.cur = None
            return None  # Regresa None si hay un error
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            if exc_type is None:
                self.conn.commit()  # Confirma los cambios si no hubo errores
            self.cur.close()
            self.conn.close()


class Cliente:
    """
    Clase para manejar los clientes en la base de datos.
    """
    def __init__(self, nombre, numero, correo, direccion):
        self.nombre = nombre
        self.numero = numero
        self.correo = correo
        self.direccion = direccion

    def CREATE(self):
        """
        Inserta un nuevo cliente en la base de datos.
        """
        try:
            with Database() as cur:
                sql = """
                INSERT INTO cliente(correo, numero_contacto, nombre, cp, cuidad, calle, numero, role)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                valores = (
                    self.correo,
                    self.numero,
                    self.nombre,
                    self.direccion["cp"],
                    self.direccion["cuidad"],
                    self.direccion["calle"],
                    self.direccion["numero"],
                    "cliente"  # Rol predeterminado
                )
                cur.execute(sql, valores)
        except Exception as e:
            print(Fore.RED + f"Error al agregar cliente: {e}")

    @classmethod
    def READ_ALL(cls):
        """
        Recupera todos los clientes de la base de datos.
        """
        try:
            with Database() as cur:
                cur.execute("SELECT * FROM cliente")
                clientes = cur.fetchall()
                return clientes
        except Exception as e:
            print(Fore.RED + f"Error al leer clientes: {e}")
            return []

    @classmethod
    def LOGIN(cls, correo, numero_contacto):
        """
        Verifica las credenciales de inicio de sesión.
        """
        try:
            with Database() as cur:
                sql = "SELECT * FROM cliente WHERE CORREO = %s AND NUMERO_CONTACTO = %s"
                cur.execute(sql, (correo, numero_contacto))
                usuario = cur.fetchone()
                return usuario
        except Exception as e:
            print(Fore.RED + f"Error al iniciar sesión: {e}")
            return None


class Producto:
    """
    Clase para manejar los productos en la base de datos.
    """
    def __init__(self, precio, color, nombre, categoria):
        self.precio = precio
        self.color = color
        self.nombre = nombre
        self.categoria = categoria

    def CREATE(self):
        """
        Inserta un nuevo producto en la base de datos.
        """
        try:
            with Database() as cur:
                sql = "INSERT INTO producto(precio, color, nombre, categoria) VALUES (%s, %s, %s, %s)"
                valores = (self.precio, self.color, self.nombre, self.categoria)
                cur.execute(sql, valores)
        except Exception as e:
            print(Fore.RED + f"Error al agregar producto: {e}")

    @classmethod
    def READ_ALL(cls):
        """
        Recupera todos los productos de la base de datos.
        """
        try:
            with Database() as cur:
                cur.execute("SELECT * FROM producto")
                productos = cur.fetchall()
                return productos
        except Exception as e:
            print(Fore.RED + f"Error al leer productos: {e}")
            return []

    @classmethod
    def DELETE(cls, producto_id):
        """
        Elimina un producto por ID.
        """
        try:
            with Database() as cur:
                sql = "DELETE FROM producto WHERE ID = %s"
                cur.execute(sql, (producto_id,))
        except Exception as e:
            print(Fore.RED + f"Error al eliminar producto: {e}")


class Ventas:
    """
    Clase para manejar las ventas en la base de datos.
    """
    def __init__(self, cliente_id, producto_id, cantidad):
        self.cliente_id = cliente_id
        self.producto_id = producto_id
        self.cantidad = cantidad

    def CREATE(self):
        """
        Inserta una nueva venta en la base de datos.
        """
        try:
            with Database() as cur:
                sql = "INSERT INTO ventas(cliente_id, producto_id, cantidad) VALUES (%s, %s, %s)"
                valores = (self.cliente_id, self.producto_id, self.cantidad)
                cur.execute(sql, valores)
        except Exception as e:
            print(Fore.RED + f"Error al registrar venta: {e}")

    @classmethod
    def READ_ALL(cls):
        """
        Recupera todas las ventas de la base de datos.
        """
        try:
            with Database() as cur:
                cur.execute("SELECT * FROM ventas")
                ventas = cur.fetchall()
                return ventas
        except Exception as e:
            print(Fore.RED + f"Error al leer ventas: {e}")
            return []
