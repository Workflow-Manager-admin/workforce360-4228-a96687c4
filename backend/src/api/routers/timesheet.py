"""
Router for Timesheet API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models, db, auth


router = APIRouter(prefix="/timesheets", tags=["timesheets"])


# PUBLIC_INTERFACE
@router.get("/", response_model=list[schemas.TimesheetEntry])
def list_timesheets(
    skip: int = 0,
    limit: int = 100,
    db_: Session = Depends(db.get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """List all timesheet entries (protected)."""
    return db_.query(models.TimesheetEntry).offset(skip).limit(limit).all()


@router.get("/{timesheet_id}", response_model=schemas.TimesheetEntry)
def get_timesheet(
    timesheet_id: int,
    db_: Session = Depends(db.get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Get timesheet by id (protected)."""
    entry = (
        db_.query(models.TimesheetEntry)
        .filter(models.TimesheetEntry.id == timesheet_id)
        .first()
    )
    if not entry:
        raise HTTPException(status_code=404, detail="Timesheet not found")
    return entry


@router.post("/", response_model=schemas.TimesheetEntry)
def create_timesheet(
    timesheet: schemas.TimesheetEntryCreate,
    db_: Session = Depends(db.get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Create a new timesheet entry (user determined from JWT)."""
    entry = models.TimesheetEntry(
        user_id=current_user.id,
        date=timesheet.date,
        hours=timesheet.hours,
        description=timesheet.description,
        task_id=timesheet.task_id,
    )
    db_.add(entry)
    db_.commit()
    db_.refresh(entry)
    return entry
