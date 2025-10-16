from flask import Flask, render_template, redirect, url_for, request, session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import pandas as pd
import json

# --- Base de Datos ---
# flask db init
# flask db migrate
# flask db upgrade
# ---------------------

app = Flask (__name__, template_folder= "templates")
app.config['SECRET_KEY']= "DESARROLLO_SISTEMAS"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

json_path = 'seguros-prestaciones.json'

# Base de Datos 
class Empresas(db.Model):
    Numero_Registro = db.Column(db.Integer, primary_key = True)
    Compañia_Seguros = db.Column(db.String (100), nullable = False)
    Año = db.Column(db.Integer)
    Mes = db.Column(db.Integer)
    Servicios = db.Column(db.Integer)
    Region = db.Column(db.String(100), nullable = False)
    Valor_Servicos = db.Column(db.Float)
    Porcentaje_Cobertura = db.Column(db.Integer)

# Abrir JSON 
with open(json_path, errors='ignore') as f:
    data = json.load(f)

df = pd.DataFrame(data)

conn = sqlite3.connect('data.db')
c = conn.cursor()
df.to_sql('tablename', conn)

# Rutas 
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        Numero_Registro = request.form['Numero_Registro']
        Compañia_Seguros = request.form['Compania_Seguros']
        if Numero_Registro == '' and Compañia_Seguros == '':
            return redirect(url_for('dashboard'))
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)