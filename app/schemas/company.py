from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CompanyCreate(BaseModel):
    name: str
    industry: Optional[str] = None


class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    industry: Optional[str] = None


class CompanyResponse(BaseModel):
    id: int
    name: str
    industry: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
