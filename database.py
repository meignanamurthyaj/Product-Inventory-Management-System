from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings  # <-- Absolute import ensures config is found

# Creates the connection engine using variables from settings
engine = create_engine(settings.database_url)

# Creates a session factory for database operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class that our models will inherit from
Base = declarative_base()

# Dependency function to provide a database session to our API routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()