def test_create_order_flow(client):
    # admin create product
    client.post("/api/auth/register", json={"email":"adm@a.com","password":"x","role":"admin"})
    tok = client.post("/api/auth/login", json={"email":"adm@a.com","password":"x"}).get_json()["token"]
    h_admin = {"Authorization": f"Bearer {tok}"}
    pid = client.post("/api/produits", headers=h_admin, json={"name":"Mouse","price":20,"stock":5}).get_json()["id"]

    # client
    client.post("/api/auth/register", json={"email":"u@u.com","password":"x"})
    tok = client.post("/api/auth/login", json={"email":"u@u.com","password":"x"}).get_json()["token"]
    h = {"Authorization": f"Bearer {tok}"}

    r = client.post("/api/commandes", headers=h, json={"items":[{"id":pid,"quantity":2}]})
    assert r.status_code == 201
