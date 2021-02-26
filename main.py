from database import *
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from routers import contact

app = FastAPI(title='Contact.ly', description='APIs for contact Apis', version='0.1')
app.mount("/static", StaticFiles(directory="static"), name="static")

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost.tiangolo.com", "https://localhost.tiangolo.com",
    "http://localhost", "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware, allow_origins=origins,
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)


class Contact(BaseModel):
    contact_id: int
    first_name: str
    last_name: str
    user_name: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "contact_id": 1,
                "first_name": "Jhon",
                "last_name": "Doe",
                "user_name": "jhon_123",
            }
        }


class ContactOut(BaseModel):
    contact_id: int
    first_name: str
    last_name: str
    user_name: str


@app.get("/")
async def root():
    return {"message": "Contact Applications!"}


app.include_router(contact.router_contacts)


@app.on_event("startup")
async def startup():
    print("Connecting...")
    if conn.is_closed():
        conn.connect()


@app.on_event("shutdown")
async def shutdown():
    print("Closing...")
    if not conn.is_closed():
        conn.close()
