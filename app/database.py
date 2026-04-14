from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Database configuration
DATABASE_URL = "sqlite:///./PersonalFinance.db"

# Create SQLAlchemy engine and sessionmaker
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
class Base(DeclarativeBase):
    pass

# Dependency for getting database session
def get_db():
    db = SessionLocal()
    try:
        yield db # <-- Yield the database session for use in the application
    finally:
        db.close() # <-- Ensure the databse session is closed after use