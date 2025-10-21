from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models.order import Order, OrderItem
from ..models.product import Product
from ..security import jwt_required, role_required

bp = Blueprint("orders", __name__)

@bp.get("")
@jwt_required
def list_orders():
    role = request.user["role"]; uid = request.user["sub"]
    q = Order.query if role == "admin" else Order.query.filter_by(user_id=uid)
    orders = q.order_by(Order.id.desc()).all()
    return jsonify([{"id":o.id,"status":o.status,"total":o.total} for o in orders])

@bp.get("/<int:oid>")
@jwt_required
def get_order(oid):
    o = Order.query.get_or_404(oid)
    if request.user["role"] != "admin" and o.user_id != request.user["sub"]:
        return jsonify(error="Forbidden"), 403
    items = [{"product_id":i.product_id,"qty":i.quantity,"unit_price":i.unit_price} for i in o.items]
    return jsonify(id=o.id, status=o.status, total=o.total, items=items)

@bp.post("")
@jwt_required
def create_order():
    d = request.get_json(force=True)
    items = d.get("items", [])
    if not items: return jsonify(error="items required"), 400
    o = Order(user_id=request.user["sub"], status="pending", total=0.0)
    db.session.add(o)
    total = 0.0
    for it in items:
        p = Product.query.get_or_404(int(it["id"]))
        qty = int(it["quantity"])
        if p.stock < qty: return jsonify(error="stock insufficient"), 409
        p.stock -= qty
        total += p.price * qty
        db.session.add(OrderItem(order=o, product_id=p.id, quantity=qty, unit_price=p.price))
    o.total = total
    db.session.commit()
    return jsonify(id=o.id, total=o.total, status=o.status), 201

@bp.patch("/<int:oid>")
@jwt_required
@role_required("admin")
def set_status(oid):
    d = request.get_json(force=True)
    o = Order.query.get_or_404(oid)
    o.status = d.get("status","pending")
    db.session.commit()
    return jsonify(ok=True)
