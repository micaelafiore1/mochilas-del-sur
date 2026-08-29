import sqlite3

DATABASE = "database/mochilas.db"


def conectar():
    conexion = sqlite3.connect(DATABASE)
    conexion.row_factory = sqlite3.Row
    return conexion


def crear_tabla_usuarios():
    conexion = conectar()

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            rol TEXT NOT NULL
        )
    """)

    conexion.commit()
    conexion.close()
    
def crear_tabla_productos():
    conexion = conectar()

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            modelo TEXT NOT NULL,
            color TEXT NOT NULL,
            talle TEXT NOT NULL,
            material TEXT NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0,
            stock_minimo INTEGER NOT NULL DEFAULT 0,
            taller TEXT NOT NULL
        )
    """)

    conexion.commit()
    conexion.close()
    
def crear_tabla_ventas():
    conexion = conectar()

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            usuario TEXT NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (producto_id) REFERENCES productos(id)
        )
    """)

    conexion.commit()
    conexion.close()
    
def crear_tabla_materias_primas():
    conexion = conectar()

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS materias_primas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            cantidad INTEGER NOT NULL DEFAULT 0,
            stock_minimo INTEGER NOT NULL DEFAULT 0,
            taller TEXT NOT NULL
        )
    """)

    conexion.commit()
    conexion.close()