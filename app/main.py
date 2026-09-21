from fastapi import Depends, FastAPI, HTTPException, Response
from pydantic import BaseModel
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .db import get_engine, get_session
from .models import Item, Warehouse

app = FastAPI(title="cicd-practice")


@app.get("/health")
def health(response: Response):
    """200 only when the database answers. A health check that skips the database lies."""
    try:
        with get_engine().connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception:
        response.status_code = 503
        return {"status": "database unreachable"}


class WarehouseIn(BaseModel):
    name: str


class ItemIn(BaseModel):
    sku: str
    quantity: int = 0
    warehouse_id: int


class ItemOut(ItemIn):
    id: int


@app.post("/warehouses", status_code=201)
def create_warehouse(body: WarehouseIn, db: Session = Depends(get_session)):
    warehouse = Warehouse(name=body.name)
    db.add(warehouse)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "warehouse name already exists")
    return {"id": warehouse.id, "name": warehouse.name}


@app.post("/items", status_code=201, response_model=ItemOut)
def create_item(body: ItemIn, db: Session = Depends(get_session)):
    if db.get(Warehouse, body.warehouse_id) is None:
        raise HTTPException(404, "warehouse not found")
    item = Item(**body.model_dump())
    db.add(item)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "sku already exists")
    return ItemOut(id=item.id, **body.model_dump())


@app.get("/items", response_model=list[ItemOut])
def list_items(db: Session = Depends(get_session)):
    rows = db.scalars(select(Item).order_by(Item.id)).all()
    return [ItemOut(id=r.id, sku=r.sku, quantity=r.quantity, warehouse_id=r.warehouse_id) for r in rows]
