"""Two small, synthetic tables. Deliberately generic: no GDI code or data."""
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


class Warehouse(Base):
    __tablename__ = "warehouse"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)

    items: Mapped[list["Item"]] = relationship(back_populates="warehouse")


class Item(Base):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[str] = mapped_column(String(40), unique=True)
    quantity: Mapped[int] = mapped_column(Integer, default=0)
    warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouse.id"))

    warehouse: Mapped[Warehouse] = relationship(back_populates="items")
