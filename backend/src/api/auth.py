"""
Authentication and JWT support for WorkForce360 backend MVP/POC.
"""

from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from . import models, db


# -- Config --
SECRET_KEY = "workforce360-dev-secret-mvp"  # For POC only, change in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24h for demo

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# PUBLIC_INTERFACE
def verify_password(plain_password, hashed_password):
    """Verify plaintext vs hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


# PUBLIC_INTERFACE
def get_password_hash(password):
    """Hash a password."""
    return pwd_context.hash(password)


# PUBLIC_INTERFACE
def authenticate_user(db_: Session, email: str, password: str) -> Optional[models.User]:
    """Authenticate user by email + password."""
    user = db_.query(models.User).filter(models.User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


# PUBLIC_INTERFACE
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a signed JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta if expires_delta else timedelta(minutes=15)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# PUBLIC_INTERFACE
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db_: Session = Depends(db.get_db)
) -> models.User:
    """Get user object from JWT token, raise if unauth."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db_.query(models.User).filter(models.User.id == user_id).first()
    if user is None or not user.is_active:
        raise credentials_exception
    return user


# PUBLIC_INTERFACE
def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    """Get current active user."""
    return current_user


# PUBLIC_INTERFACE
def get_current_active_admin(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if current_user.role and current_user.role.name == "admin":
        return current_user
    raise HTTPException(status_code=403, detail="Not enough permissions")
