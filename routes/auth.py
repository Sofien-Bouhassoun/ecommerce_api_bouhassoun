from flask import Blueprint, request, jsonify, current_app
from ..extensions import db
from ..models.user import User
import jwt, datetime

bp = Blueprint("auth", __name__)

@bp.post("/register")
def register():
    data = request.get_json(force=True)
    email, password = data.get("email"), data.get("password")
    if not email or not password:
        return jsonify(error="email & password required"), 400
    if User.query.filter_by(email=email).first():
        return jsonify(error="email exists"), 409
    u = User(email=email); u.set_password(password)
    if data.get("role") == "admin": u.role = "admin"
    db.session.add(u); db.session.commit()
    return jsonify(id=u.id, email=u.email, role=u.role), 201

@bp.post("/login")
def login():
    data = request.get_json(force=True)
    u = User.query.filter_by(email=data.get("email")).first()
    if not u or not u.check_password(data.get("password","")):
        return jsonify(error="invalid credentials"), 401
    payload = {
        "sub": u.id, "role": u.role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    }
    token = jwt.encode(payload, current_app.config["JWT_SECRET"], algorithm="HS256")
    return jsonify(token=token)
