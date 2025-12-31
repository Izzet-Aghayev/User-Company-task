from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.company import Company
from app.schemas.company import (
    CompanyCreate,
    CompanyUpdate,
    CompanyResponse
)
from app.auth.jwt import get_current_user
from app.models.user import User
from app.permissions.company import check_company_owner
from app.services.company import get_company_or_404


router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)


# Create
@router.post(
    "/create",
    response_model=CompanyResponse,
    status_code=status.HTTP_201_CREATED
)
def create_company(
    data: CompanyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    company = Company(
        name=data.name,
        industry=data.industry,
        owner_user_id=current_user.id
    )

    db.add(company)
    db.commit()
    db.refresh(company)
    return company

# Get all
@router.get(
    "/get", 
    response_model=list[CompanyResponse])
def get_companies(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return (
        db.query(Company)
        .filter(Company.owner_user_id == current_user.id)
        .all()
    )


# Get one
@router.get(
    "/get/{company_id}",
    response_model=CompanyResponse
)
def get_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    company = get_company_or_404(company_id, db)
    check_company_owner(company, current_user)
    return company


# Update
@router.patch(
    "/update/{company_id}",
    response_model=CompanyResponse
)
def update_company(
    company_id: int,
    data: CompanyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    company = get_company_or_404(company_id, db)
    check_company_owner(company, current_user)

    if data.name is not None:
        company.name = data.name
    if data.industry is not None:
        company.industry = data.industry

    db.commit()
    db.refresh(company)
    return company



# Delete
@router.delete(
    "/delete/{company_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    company = get_company_or_404(company_id, db)
    check_company_owner(company, current_user)

    db.delete(company)
    db.commit()
