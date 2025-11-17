"""
Importa empresas únicas desde la tabla `trabajos` hacia la tabla `companies`.
Genera un email placeholder y una contraseña temporal para cada empresa nueva.

Uso:
1) Asegurate de haber aplicado las migraciones (crear tabla companies):
   flask db migrate -m "Add Company model"
   flask db upgrade

2) Ejecutar el script:
   python scripts/import_companies_from_trabajo.py

El script mostrará las empresas creadas y las contraseñas temporales.
Luego, puedes cambiar el email/contraseña con un script o desde la BD.
"""
import sys
import secrets
import re

sys.path.insert(0, '.')

from app import app, db, Company, Trabajo


def slugify(name):
    # generar slug seguro para email (simple)
    s = name.lower()
    s = re.sub(r"[^a-z0-9]+", '-', s)
    s = re.sub(r"-+", '-', s).strip('-')
    if not s:
        s = 'empresa'
    return s


def import_companies():
    with app.app_context():
        # Obtener nombres únicos de compania_seguro
        rows = db.session.query(Trabajo.compania_seguro).distinct().all()
        names = [r[0] for r in rows if r[0]]

        if not names:
            print('No se encontraron empresas en la tabla `trabajos`.')
            return

        created = []
        for name in sorted(names):
            # Si ya existe en companies, saltar
            existing = Company.query.filter_by(nombre=name).first()
            if existing:
                print(f"-> Existe: {name} (id={existing.id}) - se omite")
                continue

            slug = slugify(name)
            # email placeholder: slug + @example.com
            email = f"{slug}@example.com"

            # Generar contraseña temporal
            password = secrets.token_urlsafe(8)

            company = Company(nombre=name, email=email)
            company.set_password(password)
            db.session.add(company)
            try:
                db.session.commit()
                created.append((company.id, name, email, password))
                print(f"Creada: id={company.id} - {name} - {email} - pwd={password}")
            except Exception as e:
                db.session.rollback()
                print(f"Error al crear {name}: {e}")

        if created:
            print('\nResumen:')
            for c in created:
                print(f"- id={c[0]} | {c[1]} | email={c[2]} | pwd={c[3]}")
        else:
            print('\nNo se crearon nuevas empresas.')


if __name__ == '__main__':
    import_companies()
