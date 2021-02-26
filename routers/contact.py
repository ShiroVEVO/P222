from typing import Any, List

import peewee
from fastapi import APIRouter, HTTPException, Response, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models.contact import create_contact, get_contact, list_contacts, delete_contact, update_category
from pydantic import BaseModel
from pydantic.utils import GetterDict

router_contacts = APIRouter(
    prefix="/contacts",
    tags=["contacts"]
)

templates = Jinja2Templates(directory="templates")


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class ContactModel(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


@router_contacts.get("/", response_model=List[ContactModel], summary="List of contacts",
                     description="Returns all contacts")
def get_contacts():
    return list_contacts()


@router_contacts.get("/view/{id}", response_model=ContactModel, summary="Returns a single contact")
async def view(id: int):
    contact = get_contact(id=id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router_contacts.post("/", response_model=ContactModel, summary="Create a new contact")
async def create(first_name: str, last_name: str, email: str, phone: str):
    return await create_contact(first_name=first_name, last_name=last_name, email=email, phone=phone)


@router_contacts.delete(
    "/remove/{id}",
    summary="Delete an individual contact",
    response_class=Response,
    responses={
        200: {"description": "Contact successfully deleted"},
        404: {"description": "Contact not found"},
    },
)
def remove_contact(id: int):
    del_contact = delete_contact(id)
    if del_contact is None:
        return Response(status_code=404)
    return Response(status_code=200)


@router_contacts.get("/view_html/{id}", response_class=HTMLResponse, summary="Returns a single contact in HTML")
async def view_html(request: Request, id: int):
    contact = get_contact(id=id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")

    return templates.TemplateResponse("view.html", {"request": request, "contact": contact})


@router_contacts.put("/update/{id}", summary="Update an contact")
async def update(id: int, new_lastname: str, new_email: str, new_phone: str):
    return update_category(id, new_lastname, new_email, new_phone)
# aaa
