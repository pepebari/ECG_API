from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from . import models, crud
from .config import get_users_config

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def create_database_tables():
    Base.metadata.create_all(bind=engine)

    config = get_users_config()
    db = SessionLocal()
    if not crud.get_user_by_username(db, config["admin_username"]):
        _create_admin_user(db, config)
    db.close()


def _create_admin_user(db, config):
    from .security import get_password_hash
    db_user = models.User(username=config["admin_username"],
                          hashed_password=get_password_hash(config["admin_password"]),
                          role="ADMIN")
    db.add(db_user)
    db.commit()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
