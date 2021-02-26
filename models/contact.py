from peewee import *

from .Base import BaseModel


class Contact(BaseModel):
    id = PrimaryKeyField(null=False)
    first_name = CharField(max_length=30)
    last_name = CharField(max_length=30)
    email = CharField(max_length=40)
    phone = CharField(max_length=25)

    class Meta:
        db_table = 'contacts'


async def create_contact(first_name: str, last_name: str, email: str, phone: str):
    contact_object = Contact(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
    )
    contact_object.save()
    return contact_object


def get_contact(id: int):
    return Contact.filter(Contact.id == id).first()


def list_contacts(skip: int = 0, limit: int = 100):
    return list(Contact.select().offset(skip).limit(limit))


def delete_contact(id: int):
    return Contact.delete().where(Contact.id == id).execute()


def update_category(id: int, new_lastname: str, new_email: str, new_phone: str):
    contact = Contact.get(Contact.id == id)
    contact.last_name = new_lastname
    contact.email = new_email
    contact.phone = new_phone
    contact.save()
    return contact
