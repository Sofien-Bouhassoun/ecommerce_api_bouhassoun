from ecommerce import create_app
from ecommerce.extensions import db
from ecommerce.models.user import User
from ecommerce.models.product import Category, Product

app = create_app()
with app.app_context():
    db.drop_all(); db.create_all()
    admin = User(email="admin@shop.io", role="admin"); admin.set_password("admin123")
    alice = User(email="alice@shop.io"); alice.set_password("alice123")
    db.session.add_all([admin, alice])
    cat = Category(name="Tech")
    db.session.add(cat); db.session.flush()
    db.session.add_all([
        Product(name="Laptop", price=999.0, stock=5, category=cat),
        Product(name="Mouse", price=25.0, stock=50, category=cat),
    ])
    db.session.commit()
    print("Seed OK.")
