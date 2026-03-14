from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.db import get_db
from app.models import Note, Application, User
from app.schemas import NoteRead, ApplicationRead
from app.auth import get_current_user
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/notes", tags=["notes"])

# 入力用スキーマ
class NoteCreate(BaseModel):
    content: str
    application_id: int

@router.get("/", response_model=List[NoteRead])
async def get_my_notes(current_user: User = Depends(get_current_user),
                       db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Note).join(Application).where(Application.user_id == current_user.id)
    )
    return result.scalars().all()

@router.get("/{note_id}", response_model=NoteRead)
async def get_note(note_id: int, current_user: User = Depends(get_current_user),
                   db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Note).join(Application).where(Note.id == note_id,
                                            Application.user_id == current_user.id)
    )
    note = result.scalars().first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

# 追加: ノート作成
@router.post("/", response_model=NoteRead, status_code=status.HTTP_201_CREATED)
async def create_note(note: NoteCreate, current_user: User = Depends(get_current_user),
                      db: AsyncSession = Depends(get_db)):
    # application_id が自分のアプリか確認
    result = await db.execute(
        select(Application).where(Application.id == note.application_id,
                                  Application.user_id == current_user.id)
    )
    app = result.scalars().first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found or not owned by user")

    new_note = Note(content=note.content, application_id=note.application_id)
    db.add(new_note)
    await db.commit()
    await db.refresh(new_note)
    return new_note

# 追加: ノート削除
@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: int, current_user: User = Depends(get_current_user),
                      db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Note).join(Application).where(Note.id == note_id,
                                            Application.user_id == current_user.id)
    )
    note = result.scalars().first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    await db.delete(note)
    await db.commit()
    return None