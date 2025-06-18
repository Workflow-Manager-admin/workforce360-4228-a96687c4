"""
Router for LeaveRequest API endpoints.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas, models, db

router = APIRouter(prefix="/leaves", tags=["leaves"])


# PUBLIC_INTERFACE
@router.get("/", response_model=list[schemas.LeaveRequest])
def list_leaves(skip: int = 0, limit: int = 100, db_: Session = Depends(db.get_db)):
    """List all leave requests."""
    return db_.query(models.LeaveRequest).offset(skip).limit(limit).all()


@router.post("/", response_model=schemas.LeaveRequest)
def create_leave_request(leave: schemas.LeaveRequestCreate, db_: Session = Depends(db.get_db)):
    """Create new leave request (user_id fixed to 1 for now)."""
    request = models.LeaveRequest(
        user_id=1,
        start_date=leave.start_date,
        end_date=leave.end_date,
        reason=leave.reason,
        status=leave.status
    )
    db_.add(request)
    db_.commit()
    db_.refresh(request)
    return request
