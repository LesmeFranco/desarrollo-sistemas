from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, desc
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
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

# Modelo: Empresa/Company
class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(200), nullable=False)
    creado_en = db.Column(db.DateTime, default=db.func.now())
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'company_id' not in session:
            flash('Por favor inicia sesión', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Rutas 
@app.route('/')
def index():
    if 'company_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        company = Company.query.filter_by(email=email).first()
        
        if company and company.check_password(password):
            session['company_id'] = company.id
            session['company_name'] = company.nombre
            return redirect(url_for('dashboard'))
        else:
            flash('Email o contraseña incorrectos', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    company_id = session.get('company_id')
    company = Company.query.get(company_id)
    company_name = company.nombre if company else 'Empresa'
    
    trabajos = db.session.query(Trabajo).filter_by(compania_seguro=company_name).all()
    
    total_facturado = 0
    total_cobertura = 0
    
    for trabajo in trabajos:
        facturacion = (trabajo.cantidad_servicios or 0) * (trabajo.valor_por_servicio or 0)
        cobertura = facturacion * ((trabajo.porcentaje_cobertura or 0) / 100.0)
        total_facturado += facturacion
        total_cobertura += cobertura
    
    datos = {
        'company_name': company_name,
        'trabajos': trabajos,
        'total_facturado': round(total_facturado, 2),
        'total_cobertura': round(total_cobertura, 2),
        'total_servicios': sum(t.cantidad_servicios or 0 for t in trabajos),
        'promedio_cobertura': round(sum(t.porcentaje_cobertura or 0 for t in trabajos) / len(trabajos), 2) if trabajos else 0
    }
    
    return render_template('dashboard.html', **datos)


@app.route('/reports/companies')
@login_required
def companies_report():
    company_id = session.get('company_id')
    company = Company.query.get(company_id)
    company_name = company.nombre if company else ''
    
    q = db.session.query(
        Trabajo.compania_seguro.label('CompaniaSeguro'),
        func.sum(Trabajo.cantidad_servicios * Trabajo.valor_por_servicio).label('TotalFacturado'),
        func.sum((Trabajo.cantidad_servicios * Trabajo.valor_por_servicio) * (Trabajo.porcentaje_cobertura / 100.0)).label('TotalCobertura')
    ).filter(
        Trabajo.anio.between(2023, 2025),
        Trabajo.compania_seguro == company_name
    ).group_by(Trabajo.compania_seguro).order_by(desc('TotalCobertura'))

    rows = []
    for r in q.all():
        rows.append({
            'CompaniaSeguro': r[0],
            'TotalFacturado': float(r[1] or 0),
            'TotalCobertura': float(r[2] or 0)
        })
    return render_template('companies.html', rows=rows)


@app.route('/reports/regions')
@login_required
def regions_report():
    company_id = session.get('company_id')
    company = Company.query.get(company_id)
    company_name = company.nombre if company else ''
    
    q = db.session.query(
        Trabajo.region.label('Region'),
        func.sum(Trabajo.cantidad_servicios).label('CantidadServicios')
    ).filter(
        Trabajo.anio.between(2023, 2025),
        Trabajo.compania_seguro == company_name
    ).group_by(Trabajo.region).order_by(desc('CantidadServicios'))

    rows = []
    for r in q.all():
        rows.append({
            'Region': r[0],
            'CantidadServicios': int(r[1] or 0)
        })
    return render_template('regions.html', rows=rows)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)