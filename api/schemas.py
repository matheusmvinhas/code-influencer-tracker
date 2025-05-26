from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
decimal = float  # simplificação para evitar Decimal

class BrandSchema(BaseModel):
    id: int
    name: Optional[str]
    cnpj: Optional[str]
    contact_email: Optional[str]
    website: Optional[str]
    instagram_handle: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class CreatorSchema(BaseModel):
    id: int
    cpf: Optional[str]
    username: Optional[str]
    email: Optional[str]
    instagram_handle: Optional[str]
    role: Optional[str]
    bio: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class BrandCreatorLinkSchema(BaseModel):
    id: int
    creator_id: Optional[int]
    brand_id: Optional[int]
    partnership_type: Optional[str]
    status: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class CreatorCodeSchema(BaseModel):
    id: int
    creator_id: Optional[int]
    brand_id: Optional[int]
    code: Optional[str]
    discount: Optional[decimal]
    commission: Optional[decimal]
    is_percentage: Optional[bool]
    usage_limit: Optional[int]
    times_used: Optional[int]
    status: Optional[str]
    started_at: Optional[datetime]
    disabled_at: Optional[datetime]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class OrderSchema(BaseModel):
    id: int
    external_order_id: Optional[str]
    date: Optional[date]
    brand_id: Optional[int]
    code: Optional[str]
    order_price: Optional[decimal]
    discount: Optional[decimal]
    total_paid: Optional[decimal]
    currency: Optional[str]
    status: Optional[str]
    customer_email: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class OrderLineSchema(BaseModel):
    id: int
    order_id: Optional[int]
    product_id: Optional[str]
    product_name: Optional[str]
    sku: Optional[str]
    quantity: Optional[int]
    unit_price: Optional[decimal]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True

class CommissionSchema(BaseModel):
    id: int
    creator_id: Optional[int]
    order_id: Optional[int]
    code_id: Optional[int]
    commission_value: Optional[decimal]
    status: Optional[str]
    paid_at: Optional[datetime]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True

class CodeLogSchema(BaseModel):
    id: int
    code_id: Optional[int]
    event: Optional[str]
    metadata_: Optional[dict]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
