from decimal import Decimal

from app import create_app
from app.extensions import db
from app.models import Usuario, Cliente, Producto, Venta, DetalleVenta

app = create_app()

with app.app_context():
    # Evitar duplicar datos si se ejecuta dos veces
    if Usuario.query.first():
        print("La base ya tiene datos. Nada que hacer.")
        raise SystemExit

    admin = Usuario(username="admin", rol="admin")
    admin.set_password("admin123")
    vendedor = Usuario(username="maria")
    vendedor.set_password("maria123")

    ana = Cliente(nombre="Ana Pérez", email="ana@mail.com", telefono="70000001")
    luis = Cliente(nombre="Luis Gómez", email="luis@mail.com", telefono="70000002")

    teclado = Producto(descripcion="Teclado mecánico", precio=Decimal("45.50"), stock=20)
    mouse = Producto(descripcion="Mouse inalámbrico", precio=Decimal("18.00"), stock=35)
    monitor = Producto(descripcion="Monitor 24 pulgadas", precio=Decimal("120.00"), stock=8)

    db.session.add_all([admin, vendedor, ana, luis, teclado, mouse, monitor])
    db.session.flush()  # asigna los IDs sin cerrar la transacción

    # Venta 1: Ana compra 1 teclado y 2 mouse
    v1 = Venta(cliente=ana)
    v1.detalles = [
        DetalleVenta(producto=teclado, cantidad=1, precio_unitario=teclado.precio),
        DetalleVenta(producto=mouse, cantidad=2, precio_unitario=mouse.precio),
    ]

    # Venta 2: Luis compra 1 monitor
    v2 = Venta(cliente=luis)
    v2.detalles = [
        DetalleVenta(producto=monitor, cantidad=1, precio_unitario=monitor.precio),
    ]

    db.session.add_all([v1, v2])
    db.session.commit()
    print("Datos de prueba insertados.")