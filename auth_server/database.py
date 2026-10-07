from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .config import setting


engine = create_engine(setting.database_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


# This function is your custom database gatekeeper
def get_db():
    db = SessionLocal()
    try:
        yield db  # This hands the active connection to your route function
    finally:
        db.close() # This automatically closes the connection when the route finishes!


