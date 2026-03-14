from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.db import get_db
from app.models import Application, User
from app.schemas import ApplicationRead, ApplicationCreate
from app.auth import get_current_user

router = APIRouter(prefix="/api/v1/applications", tags=["applications"])

@router.get("/", response_model=List[ApplicationRead])
async def get_my_applications(current_user: User = Depends(get_current_user),
                              db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Application).where(Application.user_id == current_user.id))
    return result.scalars().all()

@router.get("/{application_id}", response_model=ApplicationRead)
async def get_application(application_id: int, current_user: User = Depends(get_current_user),
                          db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Application).where(Application.id == application_id,
                                                        Application.user_id == current_user.id))
    app = result.scalars().first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    return app

@router.post("/", response_model=ApplicationRead, status_code=status.HTTP_201_CREATED)
async def create_application(application: ApplicationCreate,
                             current_user: User = Depends(get_current_user),
                             db: AsyncSession = Depends(get_db)):
    new_app = Application(**application.model_dump(), user_id=current_user.id)
    db.add(new_app)
    await db.commit()
    await db.refresh(new_app)
    return new_app

# 追加: アプリケーション削除
@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_application(application_id: int,
                             current_user: User = Depends(get_current_user),
                             db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Application).where(Application.id == application_id,
                                                        Application.user_id == current_user.id))
    app = result.scalars().first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    await db.delete(app)
    await db.commit()
    return None