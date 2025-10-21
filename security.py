import jwt
from functools import wraps
from flask import request, jsonify, current_app

def jwt_required(f):
    @wraps(f)
    def wrap(*a, **kw):
        h = request.headers.get("Authorization", "")
        if not h.startswith("Bearer "):
            return jsonify(error="Missing token"), 401
        token = h.split()[1]
        try:
            payload = jwt.decode(token, current_app.config["JWT_SECRET"], algorithms=["HS256"])
            request.user = payload
        except Exception:
            return jsonify(error="Invalid token"), 401
        return f(*a, **kw)
    return wrap

def role_required(role):
    def deco(f):
        @wraps(f)
        def wrap(*a, **kw):
            if getattr(request, "user", {}).get("role") != role:
                return jsonify(error="Forbidden"), 403
            return f(*a, **kw)
        return wrap
    return deco
