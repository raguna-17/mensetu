import pytest


# -------------------------
# Create application
# -------------------------
async def test_create_application(auth_client):

    payload = {
        "position": "Backend Engineer",
        "status": "applied"
    }

    response = await auth_client.post("/api/v1/applications/", json=payload)

    assert response.status_code == 201

    data = response.json()

    assert data["position"] == "Backend Engineer"
    assert data["status"] == "applied"
    assert "id" in data


# -------------------------
# Get my applications
# -------------------------
async def test_get_my_applications(auth_client):

    await auth_client.post("/api/v1/applications/", json={
        "position": "Backend",
        "status": "applied"
    })

    response = await auth_client.get("/api/v1/applications/")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert any(app["position"] == "Backend" for app in data)


# -------------------------
# Get single application
# -------------------------
async def test_get_application(auth_client):

    create_res = await auth_client.post("/api/v1/applications/", json={
        "position": "DevOps",
        "status": "applied"
    })

    app_id = create_res.json()["id"]

    response = await auth_client.get(f"/api/v1/applications/{app_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == app_id
    assert data["position"] == "DevOps"


# -------------------------
# Delete application
# -------------------------
async def test_delete_application(auth_client):

    create_res = await auth_client.post("/api/v1/applications/", json={
        "position": "Data Engineer",
        "status": "applied"
    })

    app_id = create_res.json()["id"]

    response = await auth_client.delete(f"/api/v1/applications/{app_id}")

    assert response.status_code == 204

    # 削除確認
    check = await auth_client.get(f"/api/v1/applications/{app_id}")

    assert check.status_code in (403, 404)


# -------------------------
# Unauthorized access
# -------------------------
async def test_application_requires_auth(client):

    response = await client.get("/api/v1/applications/")

    assert response.status_code == 401