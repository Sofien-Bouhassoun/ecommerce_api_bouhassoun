from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models.product import Product, Category
from ..security import jwt_required, role_required

bp = Blueprint("products", __name__)

@bp.get("")
def list_products():
    q = request.args.get("q")
    query = Product.query
    if q: query = query.filter(Product.name.ilike(f"%{q}%"))
    items = query.all()
    return jsonify([{
        "id": p.id, "name": p.name, "price": p.price,
        "stock": p.stock, "category": p.category.name if p.category else None
    } for p in items])

@bp.get("/<int:pid>")
def get_product(pid):
    p = Product.query.get_or_404(pid)
    return jsonify(id=p.id, name=p.name, description=p.description,
                   price=p.price, stock=p.stock,
                   category=p.category.name if p.category else None)

@bp.post("")
@jwt_required
@role_required("admin")
def create_product():
    d = request.get_json(force=True)
    cat = None
    if cid := d.get("category_id"):
        cat = Category.query.get(cid)
    p = Product(name=d["name"], description=d.get("description",""),
                price=float(d["price"]), stock=int(d.get("stock",0)),
                category=cat)
    db.session.add(p); db.session.commit()
    return jsonify(id=p.id), 201

@bp.put("/<int:pid>")
@jwt_required
@role_required("admin")
def update_product(pid):
    p = Product.query.get_or_404(pid)
    d = request.get_json(force=True)
    for k in ("name","description","price","stock","category_id"):
        if k in d: setattr(p, k, d[k])
    db.session.commit()
    return jsonify(ok=True)

@bp.delete("/<int:pid>")
@jwt_required
@role_required("admin")
def delete_product(pid):
    p = Product.query.get_or_404(pid)
    db.session.delete(p); db.session.commit()
    return ("", 204)
