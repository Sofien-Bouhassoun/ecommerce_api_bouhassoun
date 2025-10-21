def test_register_and_login(client):
    r = client.post("/api/auth/register", json={"email":"t@t.com","password":"x"})
    assert r.status_code == 201
    r = client.post("/api/auth/login", json={"email":"t@t.com","password":"x"})
    assert r.status_code == 200
    assert "token" in r.get_json()
