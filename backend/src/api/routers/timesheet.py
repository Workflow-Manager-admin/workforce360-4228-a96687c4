"""
Router for Timesheet API endpoints.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas, models, db

router = APIRouter(prefix="/timesheets", tags=["timesheets"])


# PUBLIC_INTERFACE
@router.get("/", response_model=list[schemas.TimesheetEntry])
def list_timesheets(skip: int = 0, limit: int = 100, db_: Session = Depends(db.get_db)):
    """List all timesheet entries."""
    return db_.query(models.TimesheetEntry).offset(skip).limit(limit).all()


@router.post("/", response_model=schemas.TimesheetEntry)
def create_timesheet(timesheet: schemas.TimesheetEntryCreate, db_: Session = Depends(db.get_db)):
    """Create a new timesheet entry (for demonstration, user id is fixed to 1)."""
    # In real logic, get user id from authenticated user
    entry = models.TimesheetEntry(
        user_id=1,
        date=timesheet.date,
        hours=timesheet.hours,
        description=timesheet.description,
        task_id=timesheet.task_id
    )
    db_.add(entry)
    db_.commit()
    db_.refresh(entry)
    return entry
