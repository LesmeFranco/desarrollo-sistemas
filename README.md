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

---

## 🚀 Guía de Uso

### Requisitos Previos

- Python 3.8+
- pip (gestor de paquetes)
- Virtual Environment (recomendado)

### Instalación Rápida

1. **Clonar el repositorio:**

```bash
git clone https://github.com/LesmeFranco/desarrollo-sistemas.git
cd desarrollo-sistemas
```

2. **Crear entorno virtual:**

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. **Instalar dependencias:**

```bash
pip install -r requirements.txt
```

4. **Configurar base de datos:**

```bash
flask db upgrade
```

5. **Importar empresas desde datos existentes:**

```bash
python scripts/import_companies_from_trabajo.py
```

Este script creará automáticamente cuentas para todas las empresas aseguradoras con contraseñas temporales.

6. **Iniciar la aplicación:**

```bash
flask --debug true run
```

Accede a: **http://localhost:5000**

---

## 📊 Funcionalidades Principales

### 🔐 Autenticación Segura

- Login multi-empresa con credenciales cifradas
- Sesiones protegidas y aislamiento de datos
- Recuperación de contraseña y cambio seguro

### 📈 Dashboard Personalizado

Cada empresa accede a:

- **Resumen ejecutivo**: Total facturado, cobertura, servicios
- **Análisis por período**: Datos de 2023-2025
- **Desglose por región**: Performance por zona geográfica
- **Tabla detallada**: Registro completo de servicios

### 🗂️ Reportes Inteligentes

- Reporte por empresa (métricas consolidadas)
- Reporte por región (análisis geográfico)
- Filtros por período y zona
- Exportación de datos (próximamente)

### ⚙️ Backend Robusto

- Base de datos relacional con SQLAlchemy ORM
- Migraciones versionadas (Alembic)
- Scripts de importación y mantenimiento
- API REST lista para integración

---

## 👥 Acceso para Empresas

### Opción 1: Crear Cuenta Manual

```bash
python scripts/register_company.py
```

Ingresa nombre de empresa, email y contraseña.

### Opción 2: Importación Automática

```bash
python scripts/import_companies_from_trabajo.py
```

Crea cuentas para todas las empresas en los datos.

### Credenciales de Prueba (después de importar)

El script mostrará un resumen con:

```
id=1 | SeguroAndes | email=seguro-andes@example.com | pwd=abc123XYZ
id=2 | ProtecSalud | email=protec-salud@example.com | pwd=def456UVW
...
```

### Flujo de Uso

1. **Empresario accede**: http://localhost:5000
2. **Ingresa credenciales**: Email + Contraseña
3. **Ve su dashboard**: Datos personalizados y privados
4. **Accede a reportes**: Análisis detallados por región y período

---

## 🔧 Configuración Avanzada

### Variables de Entorno (opcional)

Crear archivo `.env`:

```
FLASK_ENV=production
SECRET_KEY=tu-clave-secreta-aqui
DATABASE_URL=postgresql://user:password@localhost/dbname
```

### Base de Datos en Producción

Por defecto usa SQLite. Para PostgreSQL:

```bash
pip install psycopg2-binary
```

Actualizar `SQLALCHEMY_DATABASE_URI` en `app.py`

### Despliegue en Servidor

```bash
# Usar Gunicorn (producción)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## 📋 Estructura de Datos

### Tabla: companies

| Campo         | Tipo     | Descripción                  |
| ------------- | -------- | ---------------------------- |
| id            | Integer  | Identificador único          |
| nombre        | String   | Nombre de la empresa         |
| email         | String   | Email de acceso (único)      |
| password_hash | String   | Contraseña hasheada (segura) |
| creado_en     | DateTime | Fecha de creación            |

### Tabla: trabajos

| Campo               | Tipo    | Descripción                      |
| ------------------- | ------- | -------------------------------- |
| NumeroRegistro      | Integer | ID del registro                  |
| CompaniaSeguro      | String  | Nombre de la empresa aseguradora |
| Anio                | Integer | Año del servicio                 |
| Mes                 | Integer | Mes del servicio                 |
| CantidadServicios   | Integer | Cantidad de servicios prestados  |
| Region              | String  | Región geográfica                |
| ValorPorServicio    | Float   | Monto unitario                   |
| PorcentajeCobertura | Float   | % de cobertura otorgado          |

---

## 🎯 Casos de Uso

### Para Aseguradoras

✅ Monitorear performance por región en tiempo real
✅ Acceder a datos de facturación y cobertura de forma segura
✅ Análisis histórico de servicios (2023-2025)
✅ Exportar reportes para auditoría

### Para Desarrolladores

✅ Base code escalable para sistemas multi-tenant
✅ Ejemplo de integración ETL (CSV → DB → Dashboard)
✅ Arquitectura limpia con migraciones versionadas
✅ Frontend responsivo con UX moderna

---

## 📜 Licencia

Este proyecto fue desarrollado como parte de las Olimpiadas Nacionales de Informática y Electrónica (ONIET) 2025.

---
