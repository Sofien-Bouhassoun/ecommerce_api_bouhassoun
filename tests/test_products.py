def _token(client, email, pwd):
    client.post("/api/auth/register", json={"email":email,"password":pwd,"role":"admin"})
    tok = client.post("/api/auth/login", json={"email":email,"password":pwd}).get_json()["token"]
    return {"Authorization": f"Bearer {tok}"}

def test_admin_create_product(client):
    h = _token(client, "a@a.com", "x")
    r = client.post("/api/produits", headers=h, json={"name":"Kbd","price":10,"stock":3})
    assert r.status_code == 201
