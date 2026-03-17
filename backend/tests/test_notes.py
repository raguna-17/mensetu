import pytest

BASE_URL = "/api/v1/notes"


async def test_get_my_notes(client, auth_headers, test_application, db_session):
    from app.models import Note

    note = Note(content="test note", application_id=test_application.id)
    db_session.add(note)
    await db_session.commit()

    res = await client.get(f"{BASE_URL}/", headers=auth_headers)

    assert res.status_code == 200
    data = res.json()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["content"] == "test note"


async def test_get_note_detail(client, auth_headers, test_application, db_session):
    from app.models import Note

    note = Note(content="detail note", application_id=test_application.id)
    db_session.add(note)
    await db_session.commit()
    await db_session.refresh(note)

    res = await client.get(f"{BASE_URL}/{note.id}", headers=auth_headers)

    assert res.status_code == 200
    data = res.json()

    assert data["id"] == note.id
    assert data["content"] == "detail note"


async def test_get_note_not_found(client, auth_headers):
    res = await client.get(f"{BASE_URL}/9999", headers=auth_headers)

    assert res.status_code == 404
    assert res.json()["detail"] == "Note not found"


async def test_create_note(client, auth_headers, test_application):
    payload = {
        "content": "new note",
        "application_id": test_application.id,
    }

    res = await client.post(f"{BASE_URL}/", json=payload, headers=auth_headers)

    assert res.status_code == 201
    data = res.json()

    assert data["content"] == "new note"


async def test_create_note_invalid_application(client, auth_headers):
    payload = {
        "content": "bad note",
        "application_id": 9999,
    }

    res = await client.post(f"{BASE_URL}/", json=payload, headers=auth_headers)

    assert res.status_code == 404
    assert res.json()["detail"] == "Application not found or not owned by user"


async def test_create_note_unauthorized(client, test_application):
    payload = {
        "content": "no auth",
        "application_id": test_application.id,
    }

    res = await client.post(f"{BASE_URL}/", json=payload)

    assert res.status_code == 401


async def test_delete_note(client, auth_headers, test_application, db_session):
    from app.models import Note

    note = Note(content="delete me", application_id=test_application.id)
    db_session.add(note)
    await db_session.commit()
    await db_session.refresh(note)

    res = await client.delete(f"{BASE_URL}/{note.id}", headers=auth_headers)

    assert res.status_code == 204

    # 削除確認
    res = await client.get(f"{BASE_URL}/{note.id}", headers=auth_headers)
    assert res.status_code == 404


async def test_delete_note_not_found(client, auth_headers):
    res = await client.delete(f"{BASE_URL}/9999", headers=auth_headers)

    assert res.status_code == 404


# ===== 認証系 =====

async def test_notes_invalid_token(client):
    headers = {"Authorization": "Bearer invalid.token"}

    res = await client.get(f"{BASE_URL}/", headers=headers)

    assert res.status_code == 401


async def test_notes_token_user_not_found(client):
    from app.auth import create_access_token

    token = create_access_token({"sub": "9999"})
    headers = {"Authorization": f"Bearer {token}"}

    res = await client.get(f"{BASE_URL}/", headers=headers)

    assert res.status_code == 401