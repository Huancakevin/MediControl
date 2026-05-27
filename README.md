# MediControl - Sistema MVC Monolítico

Aplicación Flask monolítica para la gestión de médicos, pacientes y citas.

## Requisitos
- Python 3.10+ recomendado
- SQLite para la base de datos

## Instalación

1. Crear un ambiente virtual:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Inicializar migraciones:
   ```bash
   set FLASK_APP=app.py
   flask db init
   flask db migrate -m "initial"
   flask db upgrade
   ```
4. Ejecutar la aplicación:
   ```bash
   flask run
   ```

## Rutas principales
- `/medicos`
- `/pacientes`
- `/citas`

## Estructura MVC
- `app.py` - configuración y creación de la aplicación
- `models.py` - definiciones SQLAlchemy
- `routes.py` - controladores y rutas CRUD
- `templates/` - vistas HTML
