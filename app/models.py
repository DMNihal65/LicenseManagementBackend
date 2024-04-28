from pydantic import BaseModel
from typing import List, Optional


# Pydantic models for MongoDB documents
class User(BaseModel):
    username: str
    email: str
    password: str  # New field for storing hashed password
    company_name: Optional[str] = None
    registered_products: List[str] = []


class Product(BaseModel):
    name: str
    description: str
    price: Optional[float]
    license_type: str


class License(BaseModel):
    license_key: str
    product_id: str
    user_id: str
    issued_date: Optional[str]
    expiry_date: Optional[str]
    status: str


class ResetPasswordRequest(BaseModel):
    email: str


class ResetPassword(BaseModel):
    token: str
    new_password: str
