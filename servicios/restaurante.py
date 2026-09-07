from typing import List, Optional, Set

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class Restaurante:
    """Servicio encargado de administrar las colecciones y las reglas de negocio."""

    def __init__(
        self,
        productos_iniciales: Optional[List[Producto]] = None,
        usuarios_iniciales: Optional[List[Usuario]] = None,
        ventas_iniciales: Optional[List[Venta]] = None,
    ) -> None:
        # Listas: colecciones dinámicas de objetos que crecen y cambian en tiempo de ejecución
        self.productos: List[Producto] = list(productos_iniciales) if productos_iniciales else []
        self.usuarios: List[Usuario] = list(usuarios_iniciales) if usuarios_iniciales else []
        self._ventas: List[Venta] = list(ventas_iniciales) if ventas_iniciales else []

    # ---------------------- Productos ----------------------

    def existe_producto(self, codigo: str) -> bool:
        return any(producto.codigo == codigo for producto in self.productos)

    def registrar_producto(self, producto: Producto) -> bool:
        if self.existe_producto(producto.codigo):
            return False
        self.productos.append(producto)
        return True

    def buscar_producto(self, codigo: str) -> Optional[Producto]:
        for producto in self.productos:
            if producto.codigo == codigo:
                return producto
        return None

    def actualizar_producto(
        self,
        codigo: str,
        nombre: Optional[str] = None,
        categoria: Optional[str] = None,
        precio: Optional[float] = None,
        stock: Optional[int] = None,
    ) -> bool:
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False
        if nombre:
            producto.nombre = nombre
        if categoria:
            producto.categoria = categoria
        if precio is not None:
            producto.precio = precio
        if stock is not None:
            if stock < 0:
                raise ValueError("El stock del producto no puede ser negativo.")
            producto.stock = stock
        return True

    def eliminar_producto(self, codigo: str) -> bool:
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False
        self.productos.remove(producto)
        return True

    def listar_productos(self) -> List[Producto]:
        return list(self.productos)

    def obtener_categorias(self) -> Set[str]:
        # Conjunto: elimina automáticamente categorías repetidas
        return {producto.categoria for producto in self.productos}

    # ---------------------- Usuarios ----------------------

    def existe_usuario(self, identificacion: str) -> bool:
        return any(usuario.identificacion == identificacion for usuario in self.usuarios)

    def registrar_usuario(self, usuario: Usuario) -> bool:
        if self.existe_usuario(usuario.identificacion):
            return False
        self.usuarios.append(usuario)
        return True

    def buscar_usuario(self, identificacion: str) -> Optional[Usuario]:
        for usuario in self.usuarios:
            if usuario.identificacion == identificacion:
                return usuario
        return None

    def listar_usuarios(self) -> List[Usuario]:
        return list(self.usuarios)

    # ---------------------- Ventas ----------------------

    def vender_producto(self, codigo_producto: str, identificacion_usuario: str, cantidad: int) -> bool:
        """Registra la venta de un producto a un usuario, si es válida.

        Comprueba que el usuario y el producto existan, que la cantidad sea
        mayor que cero y que exista stock suficiente. Si todo es válido,
        crea la Venta, la agrega a la colección y disminuye el stock.
        """
        usuario = self.buscar_usuario(identificacion_usuario)
        producto = self.buscar_producto(codigo_producto)

        if usuario is None or producto is None:
            return False

        if cantidad <= 0 or producto.stock < cantidad:
            return False

        venta = Venta(usuario.identificacion, producto.codigo, cantidad)
        self._ventas.append(venta)
        producto.vender(cantidad)
        return True

    def listar_ventas(self) -> List[Venta]:
        return list(self._ventas)

    def consultar_ventas_usuario(self, identificacion_usuario: str) -> List[Venta]:
        """Recorre y filtra la colección de ventas para un usuario específico."""
        ventas_usuario: List[Venta] = []

        for venta in self._ventas:
            if venta.usuario_id == identificacion_usuario:
                ventas_usuario.append(venta)

        return ventas_usuario
