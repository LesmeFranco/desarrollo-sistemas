# Desarrollo de Sistemas - ONIET

Este sistema fue creado para resolver una consigna propuesta por la universidad Blas Pascal (Cordoba)
durante la competencia de desarrolo de sistemas de las Olimpiadas Nacionales.

Las consigas se encontrarán en ests documento:
<a href="/docs/Desarrollo-De-Sistemas-ONIET-2025_1_.pdf" rel="stylesheet" type="text">Desarrollo de Sistemas</a>

---

Este repositorio esta compuesto por los siguiente elementos:

**Estructura del repositorio**

- **`app.py`**: Punto de entrada de la aplicación (arranque del servidor y configuración básica).
- **`requirements.txt`**: Lista de dependencias Python necesarias para ejecutar el proyecto.
- **`docs/`**: Documentación y datos del proyecto. Contiene archivos como `Datos-ONIET-2025---seguros-prestaciones.csv`, `seguros-prestaciones.json` y otros recursos (PDFs, guías, datos de ejemplo).
- **`instance/`**: Carpeta para configuración sensible o específica del entorno (variables de configuración que normalmente no se suben al repositorio).
- **`migrations/`**: Scripts y metadatos de migraciones de base de datos (Alembic). Incluye `alembic.ini`, `env.py`, `script.py.mako` y las versiones de migración en `versions/`.
- **`scripts/`**: Scripts utilitarios para tareas de mantenimiento o importación de datos, por ejemplo `import_json.py` y `print_reports.py`.
- **`static/`**: Archivos estáticos que sirven las plantillas (JavaScript, CSS, imágenes). Contiene `script.js` y la carpeta `css/` con `login.css` y `style.css`.
- **`templates/`**: Plantillas HTML (Jinja2) usadas por la aplicación: `base.html`, `login.html`, `regions.html`, `companies.html`.
- **`README.md`**: Este archivo, que contiene la descripción general y las instrucciones básicas.
- **`__pycache__/`**: Carpeta con archivos compilados de Python generados automáticamente (no incluir en commits).

Notas rápidas:

- **Instalación**: Cree un entorno virtual e instale dependencias con `pip install -r requirements.txt`.
- **Ejecución**: Inicie la app con `python app.py` o según la configuración del proyecto.
- **Migraciones**: Use Alembic para gestionar migraciones; los scripts están en `migrations/`.

---
