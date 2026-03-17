import pytest

BASE_URL = "/api/v1/applications"


@pytest.mark.asyncio
async def test_get_my_applications(client, auth_headers, test_application):
    res = await client.get(BASE_URL + "/", headers=auth_headers)

    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["position"] == "Backend Engineer"


@pytest.mark.asyncio
async def test_get_application_detail(client, auth_headers, test_application):
    res = await client.get(f"{BASE_URL}/{test_application.id}", headers=auth_headers)

    assert res.status_code == 200
    data = res.json()
    assert data["id"] == test_application.id
    assert data["position"] == "Backend Engineer"


@pytest.mark.asyncio
async def test_get_application_not_found(client, auth_headers):
    res = await client.get(f"{BASE_URL}/9999", headers=auth_headers)

    assert res.status_code == 404
    assert res.json()["detail"] == "Application not found"


@pytest.mark.asyncio
async def test_create_application(client, auth_headers, test_company):
    payload = {
        "position": "Frontend Engineer",
        "status": "applied",
        "company_id": test_company.id
    }

    res = await client.post(BASE_URL + "/", json=payload, headers=auth_headers)

    assert res.status_code == 201
    data = res.json()
    assert data["position"] == "Frontend Engineer"
    assert data["status"] == "applied"


@pytest.mark.asyncio
async def test_create_application_unauthorized(client, test_company):
    payload = {
        "position": "Backend Engineer",
        "company_id": test_company.id
    }

    res = await client.post(BASE_URL + "/", json=payload)

    assert res.status_code == 401


@pytest.mark.asyncio
async def test_delete_application(client, auth_headers, test_application):
    res = await client.delete(f"{BASE_URL}/{test_application.id}", headers=auth_headers)

    assert res.status_code == 204

    # 削除確認
    res = await client.get(f"{BASE_URL}/{test_application.id}", headers=auth_headers)
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_delete_application_not_found(client, auth_headers):
    res = await client.delete(f"{BASE_URL}/9999", headers=auth_headers)

    assert res.status_code == 404