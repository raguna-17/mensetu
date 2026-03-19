from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

    applications = relationship(
        "Application",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin"
    )


class ApplicationStatus(str, enum.Enum):
    APPLIED = "applied"
    INTERVIEW = "interview"
    OFFER = "offer"
    REJECTED = "rejected"


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    industry = Column(String(100))
    created_at = Column(DateTime, server_default=func.now())

    applications = relationship(
        "Application",
        back_populates="company",
        cascade="all, delete-orphan",
        lazy="selectin"
    )


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True)
    position = Column(String(100), nullable=False)
    status = Column(
        Enum(
            ApplicationStatus,
            native_enum=False,
            values_callable=lambda obj: [e.value for e in obj]
        ),
        server_default="applied"
    )
    applied_date = Column(DateTime, server_default=func.now())
    interview_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    company_id = Column(
        Integer,
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    company = relationship(
        "Company",
        back_populates="applications",
        lazy="selectin"
    )
    user = relationship(
        "User",
        back_populates="applications",
        lazy="selectin"
    )

    notes = relationship(
        "Note",
        back_populates="application",
        cascade="all, delete-orphan",
        lazy="selectin"
    )


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    content = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    application_id = Column(
        Integer,
        ForeignKey("applications.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    application = relationship(
        "Application",
        back_populates="notes",
        lazy="selectin"
    )