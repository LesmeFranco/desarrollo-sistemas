import os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import app, db, Trabajo

with app.app_context():
    q = db.session.query(
        Trabajo.compania_seguro.label('CompaniaSeguro'),
        db.func.sum(Trabajo.cantidad_servicios * Trabajo.valor_por_servicio).label('TotalFacturado'),
        db.func.sum((Trabajo.cantidad_servicios * Trabajo.valor_por_servicio) * (Trabajo.porcentaje_cobertura / 100.0)).label('TotalCobertura')
    ).filter(Trabajo.anio.between(2023, 2025)).group_by(Trabajo.compania_seguro).order_by(db.desc('TotalCobertura'))

    print('Top companies:')
    for r in q.limit(10).all():
        print(r[0], float(r[1] or 0), float(r[2] or 0))

    q2 = db.session.query(
        Trabajo.region.label('Region'),
        db.func.sum(Trabajo.cantidad_servicios).label('CantidadServicios')
    ).filter(Trabajo.anio.between(2023, 2025)).group_by(Trabajo.region).order_by(db.desc('CantidadServicios'))

    print('\nRegions:')
    for r in q2.limit(10).all():
        print(r[0], int(r[1] or 0))
