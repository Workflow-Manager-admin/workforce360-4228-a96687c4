"""
Router for Authentication (registration, login) API endpoints using JWT.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from .. import schemas, models, db, auth


router = APIRouter(prefix="/auth", tags=["auth"])


# PUBLIC_INTERFACE
@router.post("/register", response_model=schemas.User)
def register_user(payload: schemas.UserRegister, db_: Session = Depends(db.get_db)):
    """Register a new user. Only for POC: allows open registration."""
    db_user = db_.query(models.User).filter(models.User.email == payload.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = auth.get_password_hash(payload.password)
    # Assign default "employee" role if not specified
    role_id = payload.role_id
    if not role_id:
        employee_role = db_.query(models.Role).filter(models.Role.name == "employee").first()
        if not employee_role:
            employee_role = models.Role(
                name="employee",
                description="Employee (default)"
            )
            db_.add(employee_role)
            db_.commit()
            db_.refresh(employee_role)
        role_id = employee_role.id
    user = models.User(
        username=payload.username,
        full_name=payload.full_name,
        email=payload.email,
        hashed_password=hashed_pw,
        is_active=1,
        role_id=role_id
    )
    db_.add(user)
    db_.commit()
    db_.refresh(user)
    return user


# PUBLIC_INTERFACE
@router.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db_: Session = Depends(db.get_db)
):
    """Authenticate user with email + password and issue JWT."""
    user = auth.authenticate_user(db_, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}


# PUBLIC_INTERFACE
@router.get("/me", response_model=schemas.User)
def get_me(current_user: models.User = Depends(auth.get_current_active_user)):
    """Get details for current user."""
    return current_user
