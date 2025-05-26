from sqlalchemy import Column, Integer, String, DateTime, Numeric, Boolean, Text, JSON, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Brands(Base):
    __tablename__ = "brands"
    __table_args__ = {"schema": "influencer"}

    id = Column(Integer, primary_key=True)
    name = Column(String)
    cnpj = Column(String)
    contact_email = Column(String)
    website = Column(String)
    instagram_handle = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class Creators(Base):
    __tablename__ = "creators"
    __table_args__ = {"schema": "influencer"}

    id = Column(Integer, primary_key=True)
    cpf = Column(String)
    username = Column(String)
    email = Column(String)
    instagram_handle = Column(String)
    role = Column(String)
    bio = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class BrandCreatorLinks(Base):
    __tablename__ = "brand_creator_links"
    __table_args__ = {"schema": "influencer"}

    id = Column(Integer, primary_key=True)
    creator_id = Column(Integer)
    brand_id = Column(Integer)
    partnership_type = Column(String)
    status = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class CreatorCodes(Base):
    __tablename__ = "creator_codes"
    __table_args__ = {"schema": "influencer"}

    id = Column(Integer, primary_key=True)
    creator_id = Column(Integer)
    brand_id = Column(Integer)
    code = Column(String)
    discount = Column(Numeric)
    commission = Column(Numeric)
    is_percentage = Column(Boolean)
    usage_limit = Column(Integer)
    times_used = Column(Integer)
    status = Column(String)
    started_at = Column(DateTime)
    disabled_at = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class Orders(Base):
    __tablename__ = "orders"
    __table_args__ = {"schema": "influencer"}

    id = Column(Integer, primary_key=True)
    external_order_id = Column(String)
    date = Column(Date)
    brand_id = Column(Integer)
    code = Column(String)
    order_price = Column(Numeric)
    discount = Column(Numeric)
    total_paid = Column(Numeric)
    currency = Column(String)
    status = Column(String)
    customer_email = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class OrderLines(Base):
    __tablename__ = "order_lines"
    __table_args__ = {"schema": "influencer"}

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer)
    product_id = Column(String)
    product_name = Column(String)
    sku = Column(String)
    quantity = Column(Integer)
    unit_price = Column(Numeric)
    created_at = Column(DateTime)

class Commissions(Base):
    __tablename__ = "commissions"
    __table_args__ = {"schema": "influencer"}

    id = Column(Integer, primary_key=True)
    creator_id = Column(Integer)
    order_id = Column(Integer)
    code_id = Column(Integer)
    commission_value = Column(Numeric)
    status = Column(String)
    paid_at = Column(DateTime)
    created_at = Column(DateTime)

class CodeLogs(Base):
    __tablename__ = "code_logs"
    __table_args__ = {"schema": "influencer"}

    id = Column(Integer, primary_key=True)
    code_id = Column(Integer)
    event = Column(String)
    metadata_ = Column("metadata", JSON)
    created_at = Column(DateTime)