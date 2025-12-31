from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.company import Company


def get_company_or_404(
    company_id: int,
    db: Session
) -> Company:
    company = db.query(Company).filter(Company.id == company_id).first()

    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company tapılmadı"
        )

    return company
