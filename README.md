# Mochilas del Sur

Sistema web prototipo para la gestión de productos, stock, ventas y materias primas de **Mochilas del Sur**.

## Tecnologías utilizadas

* Python 3
* Flask
* SQLite
* HTML
* CSS
* Git / GitHub

## Funcionalidades

El prototipo permite:

* Inicio de sesión de usuarios.
* Gestión de usuarios y roles.
* Consulta de productos.
* Alta de productos.
* Consulta de stock.
* Alertas de stock mínimo.
* Registro de ventas.
* Descuento automático del stock al registrar una venta.
* Validación de stock disponible.
* Historial de ventas.
* Gestión de materias primas.
* Alta de materias primas.
* Alertas de stock mínimo de materias primas.
* Dashboard con resumen del estado del inventario.

## Estructura del proyecto

```text
mochilas-del-sur/
│
├── app.py
├── database.py
├── crear_usuarios.py
├── requirements.txt
├── README.md
│
├── database/
│   └── base de datos SQLite
│
├── static/
│   └── css/
│
└── templates/
    ├── login.html
    ├── inicio.html
    ├── productos.html
    ├── agregar_producto.html
    ├── stock.html
    ├── ventas.html
    ├── historial_ventas.html
    ├── materias_primas.html
    └── agregar_materia_prima.html
```

## Requisitos

Se necesita tener instalado:

* Python 3
* Git

## Instalación

Clonar el repositorio:

```bash
git clone URL_DEL_REPOSITORIO
```

Ingresar a la carpeta:

```bash
cd mochilas-del-sur
```

Crear un entorno virtual:

### Windows

```powershell
python -m venv venv
```

Activarlo:

```powershell
.\venv\Scripts\Activate.ps1
```

Instalar las dependencias:

```powershell
pip install -r requirements.txt
```

## Preparar la base de datos

Ejecutar:

```powershell
python crear_usuarios.py
```

Este script crea las tablas necesarias y los usuarios iniciales.

## Ejecutar la aplicación

Con el entorno virtual activado:

```powershell
python app.py
```

La aplicación estará disponible en:

```text
http://127.0.0.1:5000
```

## Usuarios de prueba

### Administrador

```text
Usuario: admin
Contraseña: 1234
```

### Depósito

```text
Usuario: deposito
Contraseña: 1234
```

### Vendedor

```text
Usuario: vendedor
Contraseña: 1234
```

## Flujo principal

El sistema permite realizar el siguiente flujo:

```text
Login
  ↓
Dashboard
  ↓
Productos
  ↓
Stock
  ↓
Registrar venta
  ↓
Descontar stock
  ↓
Verificar stock mínimo
  ↓
Consultar historial de ventas
```

También permite administrar materias primas:

```text
Materias primas
  ↓
Agregar materia prima
  ↓
Consultar cantidad disponible
  ↓
Detectar stock bajo
```

## Estado del proyecto

Prototipo funcional desarrollado para fines académicos.

Actualmente se encuentra implementada la gestión básica de productos, stock, ventas y materias primas.
