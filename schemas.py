# schemas - Added validation for users and authentication Tokens

# Imports
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

# USER & AUTHENTICATION SCHEMAS
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

# PRODUCT SCHEMAS

class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    category: str = Field(..., min_length=2, max_length=50)
    price: float = Field(..., gt=0)
    quantity: int = Field(..., ge=0)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    quantity: Optional[int] = Field(None, ge=0)

class StockUpdate(BaseModel):
    quantity: int = Field(..., ge=0)

class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True