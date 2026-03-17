from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import List, Optional
from datetime import datetime
from enum import Enum as PyEnum

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str  # 生パスワード入力用

class UserRead(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str



class ApplicationStatus(str, PyEnum):
    APPLIED = "applied"
    INTERVIEW = "interview"
    OFFER = "offer"
    REJECTED = "rejected"

# Application用のベースと作成用
class ApplicationBase(BaseModel):
    position: str
    status: ApplicationStatus = ApplicationStatus.APPLIED
    applied_date: Optional[datetime] = None
    interview_date: Optional[datetime] = None

class ApplicationCreate(ApplicationBase):
    pass  # 入力用には追加フィールドなし。必要なら notes の初期値もここで指定可能


# 入力用スキーマ
class NoteCreate(BaseModel):
    content: str
    application_id: int
    
class NoteRead(BaseModel):
    id: int
    content: str

    model_config = ConfigDict(from_attributes=True)

class ApplicationRead(ApplicationBase):
    id: int
    notes: List[NoteRead] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)

# Company用のベースと作成用
class CompanyBase(BaseModel):
    name: str
    industry: Optional[str] = None

class CompanyCreate(CompanyBase):
    pass

class CompanyRead(CompanyBase):
    id: int
    applications: List[ApplicationRead] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)