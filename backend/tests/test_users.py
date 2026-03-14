import pytest

pytestmark = pytest.mark.asyncio


# -------------------------
# User register
# -------------------------
async def test_register_user(client):

    payload = {
        "email": "test@example.com",
        "password": "password123"
    }

    response = await client.post("/api/v1/users/register", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == payload["email"]
    assert "id" in data
    assert "created_at" in data


# -------------------------
# Duplicate email
# -------------------------
async def test_register_duplicate_email(client):

    payload = {
        "email": "dup@example.com",
        "password": "password123"
    }

    await client.post("/api/v1/users/register", json=payload)

    response = await client.post("/api/v1/users/register", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


# -------------------------
# Login success
# -------------------------
async def test_login_success(client):

    payload = {
        "email": "login@example.com",
        "password": "password123"
    }

    await client.post("/api/v1/users/register", json=payload)

    response = await client.post("/api/v1/users/login", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


# -------------------------
# Login fail
# -------------------------
async def test_login_invalid_password(client):

    await client.post("/api/v1/users/register", json={
        "email": "wrong@example.com",
        "password": "password123"
    })

    response = await client.post("/api/v1/users/login", json={
        "email": "wrong@example.com",
        "password": "badpassword"
    })

    assert response.status_code == 401


# -------------------------
# Get current user
# -------------------------
async def test_get_current_user(client):

    register_data = {
        "email": "me@example.com",
        "password": "password123"
    }

    await client.post("/api/v1/users/register", json=register_data)

    login_res = await client.post("/api/v1/users/login", json=register_data)

    token = login_res.json()["access_token"]

    response = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == register_data["email"]


# -------------------------
# Unauthorized access
# -------------------------
async def test_me_without_token(client):

    response = await client.get("/api/v1/users/me")

    assert response.status_code == 401