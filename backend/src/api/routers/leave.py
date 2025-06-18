"""
Router for LeaveRequest API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models, db, auth


router = APIRouter(prefix="/leaves", tags=["leaves"])


# PUBLIC_INTERFACE
@router.get("/", response_model=list[schemas.LeaveRequest])
def list_leaves(
    skip: int = 0,
    limit: int = 100,
    db_: Session = Depends(db.get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """List all leave requests (protected)."""
    return db_.query(models.LeaveRequest).offset(skip).limit(limit).all()

@router.get("/{leave_id}", response_model=schemas.LeaveRequest)
def get_leave(
    leave_id: int,
    db_: Session = Depends(db.get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Get leave by id (protected)."""
    lr = db_.query(models.LeaveRequest).filter(models.LeaveRequest.id == leave_id).first()
    if not lr:
        raise HTTPException(status_code=404, detail="Leave request not found")
    return lr



# PUBLIC_INTERFACE
@router.post("/", response_model=schemas.LeaveRequest)
def create_leave_request(
    leave: schemas.LeaveRequestCreate,
    db_: Session = Depends(db.get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Create new leave request (user from JWT)."""
    request = models.LeaveRequest(
        user_id=current_user.id,
        start_date=leave.start_date,
        end_date=leave.end_date,
        reason=leave.reason,
        status=leave.status
    )
    db_.add(request)
    db_.commit()
    db_.refresh(request)
    return request
