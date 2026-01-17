"""
Database configuration and session management for WorkForce360 backend.
Uses SQLAlchemy ORM with a SQLite database for demonstration.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./workforce360.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()

# PUBLIC_INTERFACE


def get_db():
    """Yields a new database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
