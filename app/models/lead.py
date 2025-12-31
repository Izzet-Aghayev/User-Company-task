from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
import enum
from app.database import Base


class LeadStatus(enum.Enum):
    new = "new"
    contacted = "contacted"
    closed = "closed"


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=False)
    status = Column(Enum(LeadStatus), default=LeadStatus.new)

    company_id = Column(
        Integer,
        ForeignKey("companies.id", ondelete="SET NULL"),
        nullable=True
    )

    contact_id = Column(
        Integer,
        ForeignKey("contacts.id", ondelete="SET NULL"),
        nullable=True
    )

    owner_user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    created_at = Column(DateTime, server_default=func.now())
