from pydantic import BaseModel
from typing import List, Optional

class ProductSchema(BaseModel):
    name: str
    price: float
    class Config: from_attributes = True

class ClientSchema(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    class Config: from_attributes = True

class InvoiceItemSchema(BaseModel):
    product_id: int
    quantity: int

class InvoiceSchema(BaseModel):
    client_id: int
    items: List[InvoiceItemSchema]

class UserSchema(BaseModel):
    name: str
    email: str
    password: str

class LoginSchema(BaseModel):
    email: str
    password: str
