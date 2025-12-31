from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LeadCreate(BaseModel):
    title: str
    status: Optional[str] = "new"
    company_id: Optional[int] = None
    contact_id: Optional[int] = None


class LeadUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None
    company_id: Optional[int] = None
    contact_id: Optional[int] = None


class LeadResponse(BaseModel):
    id: int
    title: str
    status: str
    company_id: Optional[int]
    contact_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True
