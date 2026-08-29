from flask import Flask, render_template, request, redirect, url_for, session
from database import conectar

app = Flask(__name__)

app.secret_key = "clave-prototipo-mochilas"
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        usuario = request.form["usuario"]
        password = request.form["password"]

        conexion = conectar()

        usuario_encontrado = conexion.execute(
            """
            SELECT * FROM usuarios
            WHERE usuario = ? AND password = ?
            """,
            (usuario, password)
        ).fetchone()

        conexion.close()

        if usuario_encontrado:
            session["usuario"] = usuario_encontrado["usuario"]
            session["rol"] = usuario_encontrado["rol"]

            return redirect(url_for("inicio"))

        return render_template(
            "login.html",
            error="Usuario o contraseña incorrectos"
        )

    return render_template("login.html")


@app.route("/inicio")
def inicio():

    if "usuario" not in session:
        return redirect(url_for("login"))

    conexion = conectar()

    cantidad_productos = conexion.execute(
        "SELECT COUNT(*) FROM productos"
    ).fetchone()[0]

    productos_stock_bajo = conexion.execute(
        """
        SELECT COUNT(*)
        FROM productos
        WHERE stock <= stock_minimo
        """
    ).fetchone()[0]

    cantidad_materias = conexion.execute(
        "SELECT COUNT(*) FROM materias_primas"
    ).fetchone()[0]

    materias_stock_bajo = conexion.execute(
        """
        SELECT COUNT(*)
        FROM materias_primas
        WHERE cantidad <= stock_minimo
        """
    ).fetchone()[0]

    conexion.close()

    return render_template(
        "inicio.html",
        cantidad_productos=cantidad_productos,
        productos_stock_bajo=productos_stock_bajo,
        cantidad_materias=cantidad_materias,
        materias_stock_bajo=materias_stock_bajo
    )

@app.route("/productos")
def productos():

    if "usuario" not in session:
        return redirect(url_for("login"))

    conexion = conectar()

    productos = conexion.execute(
        "SELECT * FROM productos"
    ).fetchall()

    conexion.close()

    return render_template(
        "productos.html",
        productos=productos
    )
    
@app.route("/stock")
def stock():

    if "usuario" not in session:
        return redirect(url_for("login"))

    conexion = conectar()

    productos = conexion.execute(
        "SELECT * FROM productos ORDER BY stock ASC"
    ).fetchall()

    conexion.close()

    return render_template(
        "stock.html",
        productos=productos
    )

@app.route("/ventas", methods=["GET", "POST"])
def ventas():

    if "usuario" not in session:
        return redirect(url_for("login"))

    conexion = conectar()

    productos = conexion.execute(
        "SELECT * FROM productos ORDER BY modelo"
    ).fetchall()

    if request.method == "POST":

        producto_id = request.form["producto_id"]
        cantidad = int(request.form["cantidad"])

        producto = conexion.execute(
            "SELECT * FROM productos WHERE id = ?",
            (producto_id,)
        ).fetchone()

        if producto is None:
            conexion.close()

            return render_template(
                "ventas.html",
                productos=productos,
                error="Producto no encontrado"
            )

        if cantidad > producto["stock"]:
            conexion.close()

            return render_template(
                "ventas.html",
                productos=productos,
                error="No hay suficiente stock disponible"
            )

        conexion.execute(
            """
            INSERT INTO ventas
            (producto_id, cantidad, usuario)
            VALUES (?, ?, ?)
            """,
            (
                producto_id,
                cantidad,
                session["usuario"]
            )
        )

        conexion.execute(
            """
            UPDATE productos
            SET stock = stock - ?
            WHERE id = ?
            """,
            (cantidad, producto_id)
        )

        conexion.commit()
        conexion.close()

        return redirect(url_for("stock"))

    conexion.close()

    return render_template(
        "ventas.html",
        productos=productos
    )

@app.route("/historial-ventas")
def historial_ventas():

    if "usuario" not in session:
        return redirect(url_for("login"))

    conexion = conectar()

    ventas = conexion.execute(
        """
        SELECT
            ventas.id,
            productos.modelo,
            productos.color,
            ventas.cantidad,
            ventas.usuario,
            ventas.fecha
        FROM ventas
        INNER JOIN productos
            ON ventas.producto_id = productos.id
        ORDER BY ventas.fecha DESC
        """
    ).fetchall()

    conexion.close()

    return render_template(
        "historial_ventas.html",
        ventas=ventas
    )
    
@app.route("/materias-primas")
def materias_primas():

    if "usuario" not in session:
        return redirect(url_for("login"))

    conexion = conectar()

    materias = conexion.execute(
        "SELECT * FROM materias_primas ORDER BY cantidad ASC"
    ).fetchall()

    conexion.close()

    return render_template(
        "materias_primas.html",
        materias=materias
    )
    
@app.route("/agregar-materia-prima", methods=["GET", "POST"])
def agregar_materia_prima():

    if "usuario" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        nombre = request.form["nombre"]
        cantidad = int(request.form["cantidad"])
        stock_minimo = int(request.form["stock_minimo"])
        taller = request.form["taller"]

        conexion = conectar()

        conexion.execute(
            """
            INSERT INTO materias_primas
            (nombre, cantidad, stock_minimo, taller)
            VALUES (?, ?, ?, ?)
            """,
            (
                nombre,
                cantidad,
                stock_minimo,
                taller
            )
        )

        conexion.commit()
        conexion.close()

        return redirect(url_for("materias_primas"))

    return render_template("agregar_materia_prima.html")

@app.route("/agregar-producto", methods=["GET", "POST"])
def agregar_producto():

    if "usuario" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        modelo = request.form["modelo"]
        color = request.form["color"]
        talle = request.form["talle"]
        material = request.form["material"]
        stock = request.form["stock"]
        stock_minimo = request.form["stock_minimo"]
        taller = request.form["taller"]

        conexion = conectar()

        conexion.execute(
            """
            INSERT INTO productos
            (modelo, color, talle, material, stock, stock_minimo, taller)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                modelo,
                color,
                talle,
                material,
                stock,
                stock_minimo,
                taller
            )
        )

        conexion.commit()
        conexion.close()

        return redirect(url_for("productos"))

    return render_template("agregar_producto.html")

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)