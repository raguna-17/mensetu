import pytest

BASE_URL = "/api/v1/companies"


@pytest.mark.asyncio
async def test_get_companies(client, test_company):
    res = await client.get(BASE_URL + "/")

    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["name"] == "Test Company"


@pytest.mark.asyncio
async def test_get_company_detail(client, test_company):
    res = await client.get(f"{BASE_URL}/{test_company.id}")

    assert res.status_code == 200
    data = res.json()
    assert data["id"] == test_company.id
    assert data["name"] == "Test Company"


@pytest.mark.asyncio
async def test_get_company_not_found(client):
    res = await client.get(f"{BASE_URL}/9999")

    assert res.status_code == 404
    assert res.json()["detail"] == "Company not found"


@pytest.mark.asyncio
async def test_create_company(client):
    payload = {
        "name": "New Company",
        "industry": "Finance"
    }

    res = await client.post(BASE_URL + "/", json=payload)

    assert res.status_code == 201
    data = res.json()
    assert data["name"] == "New Company"
    assert data["industry"] == "Finance"


@pytest.mark.asyncio
async def test_create_company_invalid(client):
    # name必須なので欠けてるパターン
    payload = {
        "industry": "IT"
    }

    res = await client.post(BASE_URL + "/", json=payload)

    assert res.status_code == 422


@pytest.mark.asyncio
async def test_delete_company(client, test_company):
    res = await client.delete(f"{BASE_URL}/{test_company.id}")

    assert res.status_code == 204

    # 削除確認
    res = await client.get(f"{BASE_URL}/{test_company.id}")
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_delete_company_not_found(client):
    res = await client.delete(f"{BASE_URL}/9999")

    assert res.status_code == 404