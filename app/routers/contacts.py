from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.jwt import get_current_user
from app.database import get_db
from app.models.contact import Contact
from app.models.user import User
from app.schemas.contact import (
    ContactCreate,
    ContactResponse,
    ContactUpdate
)


router = APIRouter(
    prefix="/contacts",
    tags=["Contacts"]
)


@router.post(
    "/create",
    response_model=ContactResponse,
    status_code=201
)
def create_contact(
    data: ContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    contact = Contact(
        **data.dict(),
        owner_user_id=current_user.id
    )

    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


@router.get(
    "/get", 
    response_model=list[ContactResponse])
def get_contacts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Contact).filter(
        Contact.owner_user_id == current_user.id
    ).all()


@router.get(
    "/get/{contact_id}",
    response_model=ContactResponse)
def get_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    contact = db.query(Contact).get(contact_id)

    if not contact:
        raise HTTPException(404, "Contact tapılmadı")

    if contact.owner_user_id != current_user.id:
        raise HTTPException(403, "İcazə yoxdur")

    return contact


@router.patch(
    "/update/{contact_id}", 
    response_model=ContactResponse)
def update_contact(
    contact_id: int,
    data: ContactUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    contact = db.query(Contact).get(contact_id)

    if not contact:
        raise HTTPException(404)

    if contact.owner_user_id != current_user.id:
        raise HTTPException(403)

    for key, value in data.dict(exclude_unset=True).items():
        setattr(contact, key, value)

    db.commit()
    db.refresh(contact)
    return contact


@router.delete(
    "/delete/{contact_id}", 
    status_code=204)
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    contact = db.query(Contact).get(contact_id)

    if not contact:
        raise HTTPException(404)

    if contact.owner_user_id != current_user.id:
        raise HTTPException(403)

    db.delete(contact)
    db.commit()

