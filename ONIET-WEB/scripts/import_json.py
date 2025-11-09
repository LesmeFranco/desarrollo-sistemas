import json
import os
import sys

# Ensure repo root is on sys.path so imports like `import app` work when running this script
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import app, db, Trabajo, json_path


def normalize_value(v):
    # Helper to convert empty strings to None
    if v == "" or v is None:
        return None
    return v


def import_json(path=json_path):
    if not os.path.exists(path):
        print(f"JSON file not found: {path}")
        return

    # use utf-8-sig to gracefully handle BOM if present
    with open(path, errors='ignore', encoding='utf-8-sig') as f:
        data = json.load(f)

    trabajos = []
    for row in data:
        try:
            t = Trabajo(
                numero_registro=int(normalize_value(row.get('NumeroRegistro'))),
                compania_seguro=str(normalize_value(row.get('CompaniaSeguro') or row.get('CompaniaSeguro'))).strip(),
                anio=int(normalize_value(row.get('Anio') or row.get('Año'))),
                mes=int(normalize_value(row.get('Mes'))),
                cantidad_servicios=int(normalize_value(row.get('CantidadServicios') or row.get('Servicios')) or 0),
                region=str(normalize_value(row.get('Region'))).strip(),
                valor_por_servicio=float(normalize_value(row.get('ValorPorServicio') or row.get('Valor_Servicos') or row.get('ValorPorServicio')) or 0.0),
                porcentaje_cobertura=float(normalize_value(row.get('PorcentajeCobertura')) or 0.0)
            )
            trabajos.append(t)
        except Exception as e:
            print(f"Skipping row due to error: {e} -- row: {row}")

    if trabajos:
        with app.app_context():
            # Optionally clear existing table? here we append
            db.session.bulk_save_objects(trabajos)
            db.session.commit()
            print(f"Imported {len(trabajos)} rows into trabajos table.")
    else:
        print("No rows to import.")


if __name__ == '__main__':
    import_json()
