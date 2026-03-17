from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import List, Optional
from datetime import datetime
from enum import Enum as PyEnum

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str  # 逕溘ヱ繧ｹ繝ｯ繝ｼ繝牙・蜉帷畑

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

# Application逕ｨ縺ｮ繝吶・繧ｹ縺ｨ菴懈・逕ｨ
class ApplicationBase(BaseModel):
    position: str
    status: ApplicationStatus = ApplicationStatus.APPLIED
    applied_date: Optional[datetime] = None
    interview_date: Optional[datetime] = None

class ApplicationCreate(ApplicationBase):
    pass  # 蜈･蜉帷畑縺ｫ縺ｯ霑ｽ蜉繝輔ぅ繝ｼ繝ｫ繝峨↑縺励ょｿ・ｦ√↑繧・notes 縺ｮ蛻晄悄蛟､繧ゅ％縺薙〒謖・ｮ壼庄閭ｽ


# 蜈･蜉帷畑繧ｹ繧ｭ繝ｼ繝・
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

# Company逕ｨ縺ｮ繝吶・繧ｹ縺ｨ菴懈・逕ｨ
class CompanyBase(BaseModel):
    name: str
    industry: Optional[str] = None

class CompanyCreate(CompanyBase):
    pass

class CompanyRead(CompanyBase):
    id: int
    applications: List[ApplicationRead] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)

