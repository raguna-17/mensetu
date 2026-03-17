import pytest



async def test_register_success(client):
    payload = {
        "email": "newuser@example.com",
        "password": "password123"
    }

    res = await client.post("/api/v1/users/register", json=payload)

    assert res.status_code == 200
    data = res.json()

    assert data["email"] == payload["email"]
    assert "id" in data



async def test_register_duplicate_email(client, test_user):
    payload = {
        "email": test_user.email,
        "password": "password123"
    }

    res = await client.post("/api/v1/users/register", json=payload)

    assert res.status_code == 400
    assert res.json()["detail"] == "Email already registered"



async def test_login_success(client, test_user):
    payload = {
        "email": test_user.email,
        "password": "password"
    }

    res = await client.post("/api/v1/users/login", json=payload)

    assert res.status_code == 200

    data = res.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"



async def test_login_invalid_email(client):
    payload = {
        "email": "notfound@example.com",
        "password": "password"
    }

    res = await client.post("/api/v1/users/login", json=payload)

    assert res.status_code == 401
    assert res.json()["detail"] == "Invalid credentials"



async def test_login_wrong_password(client, test_user):
    payload = {
        "email": test_user.email,
        "password": "wrongpassword"
    }

    res = await client.post("/api/v1/users/login", json=payload)

    assert res.status_code == 401
    assert res.json()["detail"] == "Invalid credentials"



async def test_read_current_user_success(client, auth_headers):
    res = await client.get("/api/v1/users/me", headers=auth_headers)

    assert res.status_code == 200

    data = res.json()

    assert "email" in data
    assert "id" in data



async def test_read_current_user_no_token(client):
    res = await client.get("/api/v1/users/me")

    assert res.status_code == 401

