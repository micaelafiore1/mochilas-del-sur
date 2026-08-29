import sqlite3
from database import (
    conectar,
    crear_tabla_usuarios,
    crear_tabla_productos,
    crear_tabla_ventas,
    crear_tabla_materias_primas
)
crear_tabla_usuarios()
crear_tabla_productos()
crear_tabla_ventas()
crear_tabla_materias_primas()

conexion = conectar()

usuarios = [
    ("admin", "1234", "Administrador"),
    ("deposito", "1234", "Encargado de depósito"),
    ("vendedor", "1234", "Vendedor")
]

for usuario, password, rol in usuarios:
    try:
        conexion.execute(
            """
            INSERT INTO usuarios (usuario, password, rol)
            VALUES (?, ?, ?)
            """,
            (usuario, password, rol)
        )
    except sqlite3.IntegrityError:
        pass

productos = [
    ("Mochila Urbana", "Negro", "Mediana", "Nylon", 15, 5, "Taller Central"),
    ("Mochila Urbana", "Azul", "Mediana", "Nylon", 8, 5, "Taller Central"),
    ("Mochila Escolar", "Rojo", "Grande", "Poliéster", 3, 5, "Taller Norte"),
    ("Bolso de Viaje", "Negro", "Grande", "Lona", 12, 4, "Taller Sur"),
    ("Funda Tablet", "Gris", "Única", "Neopreno", 20, 5, "Taller Central")
]

cantidad_productos = conexion.execute(
    "SELECT COUNT(*) FROM productos"
).fetchone()[0]

if cantidad_productos == 0:

    for producto in productos:
        conexion.execute(
            """
            INSERT INTO productos
            (modelo, color, talle, material, stock, stock_minimo, taller)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            producto
        )

conexion.execute(
    """
    UPDATE materias_primas
    SET taller = ?
    WHERE taller = ?
    """,
    ("Taller Central", "Ta")
)

conexion.commit()
conexion.close()
    
print("usuarios y productos creados correctamente.")