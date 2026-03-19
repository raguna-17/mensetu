from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import List, Optional
from datetime import datetime
from enum import Enum as PyEnum


# -----------------
# User
# -----------------

class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(min_length=4, max_length=22)


class UserRead(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# -----------------
# Enum（共通化推奨）
# -----------------

class ApplicationStatus(str, PyEnum):
    APPLIED = "applied"
    INTERVIEW = "interview"
    OFFER = "offer"
    REJECTED = "rejected"


# -----------------
# Note
# -----------------

class NoteCreate(BaseModel):
    content: str = Field(max_length=1000)
    application_id: int

class NoteRead(BaseModel):
    id: int
    content: str
    application_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# -----------------
# Application
# -----------------

class ApplicationBase(BaseModel):
    position: str = Field(max_length=100)
    applied_date: Optional[datetime] = None
    interview_date: Optional[datetime] = None


class ApplicationCreate(BaseModel):
    position: str = Field(max_length=100)
    company_id: int
    status: ApplicationStatus = ApplicationStatus.APPLIED

class ApplicationRead(ApplicationBase):
    id: int
    status: ApplicationStatus
    created_at: datetime
    notes: List[NoteRead] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


# 軽量版（ネスト爆発防止）
class ApplicationSimple(BaseModel):
    id: int
    position: str

    model_config = ConfigDict(from_attributes=True)


# -----------------
# Company
# -----------------

class CompanyBase(BaseModel):
    name: str = Field(max_length=100)
    industry: Optional[str] = Field(default=None, max_length=100)


class CompanyCreate(CompanyBase):
    pass


class CompanyRead(CompanyBase):
    id: int
    created_at: datetime
    applications: List[ApplicationSimple] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)