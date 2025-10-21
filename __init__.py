from flask import Flask, jsonify
from .extensions import db
from .routes.auth import bp as auth_bp
from .routes.products import bp as products_bp
from .routes.orders import bp as orders_bp
from .models import user, product, order  # register models

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    db.init_app(app)

    @app.errorhandler(404)
    def _404(e): return (jsonify(error="Not Found"), 404)
    @app.errorhandler(400)
    def _400(e): return (jsonify(error="Bad Request"), 400)

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(products_bp, url_prefix="/api/produits")
    app.register_blueprint(orders_bp, url_prefix="/api/commandes")
    with app.app_context():
        db.create_all()
    return app
