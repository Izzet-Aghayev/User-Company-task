from fastapi import HTTPException, status
from app.models.company import Company
from app.models.user import User


def check_company_owner(
    company: Company,
    current_user: User
):
    if company.owner_user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bu əməliyyat üçün icazən yoxdur"
        )


def admin_required(user: User):
    if user.email != "admin@example.com":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin icazəsi tələb olunur"
        )