"""
Script para registrar nuevas empresas en la base de datos.
Uso: python scripts/register_company.py
"""
import sys
sys.path.insert(0, '.')

from app import app, db, Company

def register_company():
    with app.app_context():
        print("\n=== REGISTRO DE NUEVA EMPRESA ===\n")
        
        nombre = input("Nombre de la empresa: ").strip()
        if not nombre:
            print("Error: El nombre no puede estar vacío")
            return
        
        # Verificar si la empresa ya existe
        if Company.query.filter_by(nombre=nombre).first():
            print(f"Error: La empresa '{nombre}' ya existe")
            return
        
        email = input("Email de la empresa: ").strip()
        if not email or '@' not in email:
            print("Error: Ingresa un email válido")
            return
        
        # Verificar si el email ya existe
        if Company.query.filter_by(email=email).first():
            print(f"Error: El email '{email}' ya está registrado")
            return
        
        password = input("Contraseña (mínimo 6 caracteres): ").strip()
        if len(password) < 6:
            print("Error: La contraseña debe tener al menos 6 caracteres")
            return
        
        password_confirm = input("Confirmar contraseña: ").strip()
        if password != password_confirm:
            print("Error: Las contraseñas no coinciden")
            return
        
        # Crear la empresa
        try:
            company = Company(nombre=nombre, email=email)
            company.set_password(password)
            db.session.add(company)
            db.session.commit()
            print(f"\n✓ Empresa '{nombre}' registrada exitosamente")
            print(f"  Email: {email}")
        except Exception as e:
            db.session.rollback()
            print(f"Error al registrar la empresa: {e}")

if __name__ == '__main__':
    register_company()
