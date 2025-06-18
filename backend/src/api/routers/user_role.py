"""
Router for User & Role API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas, models, db

router = APIRouter(prefix="/users", tags=["users"])


# PUBLIC_INTERFACE
@router.get("/", response_model=list[schemas.User])
def list_users(skip: int = 0, limit: int = 100, db_: Session = Depends(db.get_db)):
    """List all users."""
    return db_.query(models.User).offset(skip).limit(limit).all()


@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db_: Session = Depends(db.get_db)):
    """Create a new user."""
    db_user = db_.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    fake_hashed_password = "notsecure-" + user.password  # Placeholder only!
    new_user = models.User(
        username=user.username,
        full_name=user.full_name,
        email=user.email,
        hashed_password=fake_hashed_password,
        role_id=user.role_id,
    )
    db_.add(new_user)
    db_.commit()
    db_.refresh(new_user)
    return new_user


@router.get("/roles/", response_model=list[schemas.Role])
def list_roles(db_: Session = Depends(db.get_db)):
    """List all roles."""
    return db_.query(models.Role).all()


@router.post("/roles/", response_model=schemas.Role)
def create_role(role: schemas.RoleCreate, db_: Session = Depends(db.get_db)):
    """Create a new role."""
    db_role = db_.query(models.Role).filter(models.Role.name == role.name).first()
    if db_role:
        raise HTTPException(status_code=400, detail="Role already exists")
    new_role = models.Role(name=role.name, description=role.description)
    db_.add(new_role)
    db_.commit()
    db_.refresh(new_role)
    return new_role
