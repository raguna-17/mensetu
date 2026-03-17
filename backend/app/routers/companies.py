from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.db import get_db
from app.models import Company
from app.schemas import CompanyRead, CompanyCreate

router = APIRouter(prefix="/api/v1/companies", tags=["companies"])

@router.get("/", response_model=List[CompanyRead])
async def get_companies(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Company))
    return result.scalars().all()

@router.get("/{company_id}", response_model=CompanyRead)
async def get_company(company_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Company).where(Company.id == company_id))
    company = result.scalars().first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

# 追加: 会社作�E
@router.post("/", response_model=CompanyRead, status_code=status.HTTP_201_CREATED)
async def create_company(company: CompanyCreate, db: AsyncSession = Depends(get_db)):
    new_company = Company(**company.dict())
    db.add(new_company)
    await db.commit()
    await db.refresh(new_company)
    return new_company

# 追加: 会社削除
@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(company_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Company).where(Company.id == company_id))
    company = result.scalars().first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    await db.delete(company)
    await db.commit()
    return None

