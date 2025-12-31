from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

from app.routers import auth, companies, contacts, leads
from app.database import engine, Base
from app.models import user 



app = FastAPI(
    title="Simple CRM API",
    swagger_ui_parameters={"persistAuthorization": True}
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(companies.router)
app.include_router(contacts.router)
app.include_router(leads.router)

@app.get("/")
def root():
    return {"message": "CRM API işləyir"}
