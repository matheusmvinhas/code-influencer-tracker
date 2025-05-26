from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from api.database import get_db
from api.models import (
    Brands, Creators, BrandCreatorLinks, CreatorCodes,
    Orders, OrderLines, Commissions, CodeLogs
)
from api.schemas import (
    BrandSchema, CreatorSchema, BrandCreatorLinkSchema, CreatorCodeSchema,
    OrderSchema, OrderLineSchema, CommissionSchema, CodeLogSchema
)

router = APIRouter()

# ===== Brands =====
@router.get("/brands", response_model=List[BrandSchema])
def list_brands(db: Session = Depends(get_db)):
    try:
        print("== INICIANDO QUERY ==")
        result = db.query(Brands).all()
        print(f"== RESULTADO: {result} ==")
        return result
    except Exception as e:
        import traceback
        print("== ERRO DURANTE LISTAGEM DE BRANDS ==")
        traceback.print_exc()
        raise e

@router.post("/brands", response_model=BrandSchema)
def create_brand(brand: BrandSchema, db: Session = Depends(get_db)):
    obj = Brands(**brand.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

# ===== Creators =====
@router.get("/creators", response_model=List[CreatorSchema])
def list_creators(db: Session = Depends(get_db)):
    return db.query(Creators).all()

@router.post("/creators", response_model=CreatorSchema)
def create_creator(creator: CreatorSchema, db: Session = Depends(get_db)):
    obj = Creators(**creator.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

# ===== BrandCreatorLinks =====
@router.get("/brand_creator_links", response_model=List[BrandCreatorLinkSchema])
def list_links(db: Session = Depends(get_db)):
    return db.query(BrandCreatorLinks).all()

@router.post("/brand_creator_links", response_model=BrandCreatorLinkSchema)
def create_link(link: BrandCreatorLinkSchema, db: Session = Depends(get_db)):
    obj = BrandCreatorLinks(**link.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

# ===== CreatorCodes =====
@router.get("/creator_codes", response_model=List[CreatorCodeSchema])
def list_codes(db: Session = Depends(get_db)):
    return db.query(CreatorCodes).all()

@router.post("/creator_codes", response_model=CreatorCodeSchema)
def create_code(code: CreatorCodeSchema, db: Session = Depends(get_db)):
    obj = CreatorCodes(**code.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

# ===== Orders =====
@router.get("/orders", response_model=List[OrderSchema])
def list_orders(db: Session = Depends(get_db)):
    return db.query(Orders).all()

@router.post("/orders", response_model=OrderSchema)
def create_order(order: OrderSchema, db: Session = Depends(get_db)):
    obj = Orders(**order.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

# ===== OrderLines =====
@router.get("/order_lines", response_model=List[OrderLineSchema])
def list_order_lines(db: Session = Depends(get_db)):
    return db.query(OrderLines).all()

@router.post("/order_lines", response_model=OrderLineSchema)
def create_order_line(line: OrderLineSchema, db: Session = Depends(get_db)):
    obj = OrderLines(**line.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

# ===== Commissions =====
@router.get("/commissions", response_model=List[CommissionSchema])
def list_commissions(db: Session = Depends(get_db)):
    return db.query(Commissions).all()

@router.post("/commissions", response_model=CommissionSchema)
def create_commission(c: CommissionSchema, db: Session = Depends(get_db)):
    obj = Commissions(**c.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

# ===== CodeLogs =====
@router.get("/code_logs", response_model=List[CodeLogSchema])
def list_logs(db: Session = Depends(get_db)):
    return db.query(CodeLogs).all()

@router.post("/code_logs", response_model=CodeLogSchema)
def create_log(log: CodeLogSchema, db: Session = Depends(get_db)):
    obj = CodeLogs(**log.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj