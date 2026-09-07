# restaurante_app — Semana 11

**Estudiante:** Walter Ortiz
**Asignatura:** Programación Orientada a Objetos
**Actividad:** Tarea Semana 11 — Fundamentos de colecciones aplicados a relaciones, ventas
y persistencia JSON

## Descripción del sistema

`restaurante_app` es un sistema de consola para administrar productos, usuarios y ventas de
un restaurante. En esta entrega se incorpora la **operación de venta**, que relaciona a un
usuario con un producto, controla el stock disponible y queda registrada en una colección de
objetos `Venta`. La persistencia en JSON se amplía para conservar **productos, usuarios y
ventas**.

## Estructura del proyecto


## Responsabilidad de los componentes

- **`modelos/producto.py`**: define `Producto`, ahora con un atributo `stock` (validado para
  que nunca sea negativo) y un método `vender(cantidad)` que disminuye el stock. Incluye
  `to_dict()` / `from_dict()` para JSON.
- **`modelos/usuario.py`**: define `Usuario` con sus validaciones (identificación, nombre y
  correo), y `to_dict()` / `from_dict()` para persistirlo en JSON.
- **`modelos/venta.py`**: define `Venta`, que guarda `usuario_id`, `producto_codigo` y
  `cantidad`, representando la relación entre un usuario y un producto vendido.
- **`servicios/archivo_servicio.py`**: centraliza la lectura y escritura de `productos.json`,
  `usuarios.json` y `ventas.json`, usando `with open()`, UTF-8, `json.load()` y `json.dump()`.
- **`servicios/restaurante.py`**: administra las colecciones de productos, usuarios y ventas.
  Incluye `vender_producto()` (valida usuario, producto, cantidad y stock antes de registrar
  la venta) y `consultar_ventas_usuario()` (recorre y filtra la colección de ventas).
- **`main.py`**: coordina el menú, carga las tres colecciones al iniciar y guarda los archivos
  correspondientes después de cada operación que modifica productos, usuarios o ventas.

## Stock y relación Usuario–Producto mediante Venta

Cada `Producto` tiene un `stock` que representa la cantidad disponible. Al vender:

1. Se busca al usuario por su identificación y al producto por su código.
2. Se valida que ambos existan, que la cantidad sea mayor que cero y que haya stock
   suficiente.
3. Se crea una `Venta(usuario_id, producto_codigo, cantidad)` y se agrega a la colección de
   ventas.
4. Se llama a `producto.vender(cantidad)`, que descuenta el stock.
5. Se guardan `ventas.json` y `productos.json` (una sola operación modifica dos colecciones).

La consulta de ventas por usuario recorre la colección de ventas y filtra únicamente las que
coinciden con la identificación indicada, mostrando el código del producto, su nombre y la
cantidad adquirida.

## Persistencia de productos, usuarios y ventas

**Guardado:** cada objeto se convierte a diccionario con `to_dict()`, se arma una lista de
diccionarios y se escribe con `json.dump()` en su archivo correspondiente.

**Carga (al iniciar):** se lee cada archivo con `json.load()`, y cada diccionario válido se
reconstruye como objeto (`Producto.from_dict()`, `Usuario.from_dict()`, `Venta.from_dict()`)
antes de entregarse al servicio `Restaurante`.

- Registrar, actualizar o eliminar un producto → se guarda `productos.json`.
- Registrar un usuario → se guarda `usuarios.json`.
- Realizar una venta → se guardan `ventas.json` **y** `productos.json` (por el cambio de
  stock).

## Excepciones controladas

- **`FileNotFoundError`**: si alguno de los tres archivos JSON no existe todavía, esa
  colección inicia vacía sin detener el programa.
- **`json.JSONDecodeError`**: si un archivo existe pero su contenido no es JSON válido, se
  informa el problema y esa colección inicia vacía.
- **`PermissionError`**: se controla tanto al leer como al escribir cada archivo.
- **`KeyError`**: si un registro guardado no tiene alguna clave esperada, ese registro se
  omite con un aviso, sin afectar al resto de la colección.
- **`ValueError`**: las validaciones de `Producto` (campos vacíos, precio o stock negativo),
  `Usuario` (campos vacíos, formato de correo) y `Venta` (cantidad no positiva, referencias
  vacías) lanzan `ValueError`; se captura tanto al reconstruir desde JSON como al operar desde
  el menú, sin detener la aplicación.

## Cómo ejecutar el programa

1. Ubicarse en la carpeta `restaurante_app/`.
2. Ejecutar:
   3. Usar el menú numérico para registrar y administrar productos y usuarios, vender productos,
   consultar las ventas de un usuario y mostrar las categorías registradas.

## Pruebas realizadas

1. Se registró un usuario y un producto con stock inicial de 10 unidades.
2. Se realizó una venta de 2 unidades: el sistema confirmó la venta, el stock bajó a 8, y
   `ventas.json` registró la operación con el usuario, el producto y la cantidad.
3. Se consultaron las ventas del usuario y se mostró correctamente el producto comprado.
4. Se cerró el programa y se volvió a ejecutar: se confirmó que productos, usuarios y ventas
   se recuperaron correctamente, con el stock actualizado en 8.
5. Se intentó vender 100 unidades del mismo producto (más de lo disponible): la operación fue
   rechazada con un mensaje claro, y se comprobó que el stock y los archivos JSON no se vieron
   alterados por el intento fallido.
