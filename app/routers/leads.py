from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.jwt import get_current_user
from app.models.lead import Lead
from app.schemas.lead import LeadCreate, LeadUpdate, LeadResponse
from app.models.user import User
from app.models.contact import Contact

router = APIRouter(
    prefix="/leads", 
    tags=["Leads"]
    )


@router.post(
    "/create", 
    response_model=LeadResponse, status_code=status.HTTP_201_CREATED)
def create_lead(
    payload: LeadCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    lead = Lead(
        **payload.model_dump(),
        owner_user_id=current_user.id
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead


@router.get(
    "/get", 
    response_model=list[LeadResponse])
def get_leads(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return (
        db.query(Lead)
        .filter(Lead.owner_user_id == current_user.id)
        .all()
    )


@router.get(
    "/get/{lead_id}", 
    response_model=LeadResponse)
def get_lead(
    lead_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    if lead.owner_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    return lead


@router.patch(
    "/update/{lead_id}",
    response_model=LeadResponse
)
def update_lead(
    lead_id: int,
    payload: LeadUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()

    if not lead:
        raise HTTPException(status_code=404, detail="Lead tapılmadı")

    if lead.owner_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    data = payload.model_dump(exclude_unset=True)

    # 🔒 ƏGƏR contact_id dəyişdirilirsə — YOXLA
    if "contact_id" in data and data["contact_id"] is not None:
        contact = (
            db.query(Contact)
            .filter(Contact.id == data["contact_id"])
            .first()
        )

        if not contact:
            raise HTTPException(
                status_code=404,
                detail="Contact tapılmadı"
            )

        if contact.owner_user_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="Başqa istifadəçinin əlaqə məlumatlarını təyin edə bilməzsiniz"
            )

    # 🔁 SAFE UPDATE
    for key, value in data.items():
        setattr(lead, key, value)

    db.commit()
    db.refresh(lead)
    return lead


@router.delete(
    "/delete/{lead_id}", 
    status_code=status.HTTP_204_NO_CONTENT)
def delete_lead(
    lead_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    if lead.owner_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    db.delete(lead)
    db.commit()
