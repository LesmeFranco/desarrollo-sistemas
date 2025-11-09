from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, desc
import json

# --- Base de Datos ---
# flask db init
# flask db migrate
# flask db upgrade
# ---------------------

app = Flask(__name__, template_folder="templates")
app.config['SECRET_KEY'] = "DESARROLLO_SISTEMAS"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Path al JSON (usado por el script de importación o por pruebas)
json_path = "docs/seguros-prestaciones.json"

# Modelo SQLAlchemy preparado para migraciones
class Trabajo(db.Model):
    __tablename__ = 'trabajos'
    numero_registro = db.Column('NumeroRegistro', db.Integer, primary_key=True)
    compania_seguro = db.Column('CompaniaSeguro', db.String(100), nullable=False)
    anio = db.Column('Anio', db.Integer)
    mes = db.Column('Mes', db.Integer)
    cantidad_servicios = db.Column('CantidadServicios', db.Integer)
    region = db.Column('Region', db.String(100), nullable=False)
    valor_por_servicio = db.Column('ValorPorServicio', db.Float)
    porcentaje_cobertura = db.Column('PorcentajeCobertura', db.Float)

# Rutas 
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        Numero_Registro = request.form.get('Numero_Registro', '')
        Compañia_Seguros = request.form.get('Compania_Seguros', '')
        # lógica de ejemplo; la app real debe validar y setear session
        if Numero_Registro == '' and Compañia_Seguros == '':
            return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/reports/companies')
def companies_report():
    # Agrega filtro por años 2023-2025 según enunciado
    q = db.session.query(
        Trabajo.compania_seguro.label('CompaniaSeguro'),
        func.sum(Trabajo.cantidad_servicios * Trabajo.valor_por_servicio).label('TotalFacturado'),
        func.sum((Trabajo.cantidad_servicios * Trabajo.valor_por_servicio) * (Trabajo.porcentaje_cobertura / 100.0)).label('TotalCobertura')
    ).filter(Trabajo.anio.between(2023, 2025)).group_by(Trabajo.compania_seguro).order_by(desc('TotalCobertura'))

    rows = []
    for r in q.all():
        rows.append({
            'CompaniaSeguro': r[0],
            'TotalFacturado': float(r[1] or 0),
            'TotalCobertura': float(r[2] or 0)
        })
    return render_template('companies.html', rows=rows)


@app.route('/reports/regions')
def regions_report():
    q = db.session.query(
        Trabajo.region.label('Region'),
        func.sum(Trabajo.cantidad_servicios).label('CantidadServicios')
    ).filter(Trabajo.anio.between(2023, 2025)).group_by(Trabajo.region).order_by(desc('CantidadServicios'))

    rows = []
    for r in q.all():
        rows.append({
            'Region': r[0],
            'CantidadServicios': int(r[1] or 0)
        })
    return render_template('regions.html', rows=rows)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)