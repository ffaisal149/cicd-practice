"""Database wiring. The connection string comes from the environment, the way GDI does it."""
import os
from functools import lru_cache

from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Predictable constraint names, so Alembic can track them (Stage 7 explains why).
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING_CONVENTION)


def database_url() -> str:
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL is not set. See the README.")
    return url


@lru_cache
def get_engine():
    return create_engine(database_url(), pool_pre_ping=True)


def get_session():
    session = sessionmaker(bind=get_engine())()
    try:
        yield session
    finally:
        session.close()
