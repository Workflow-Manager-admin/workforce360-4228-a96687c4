"""
Router for Task API endpoints.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import schemas, models, db

router = APIRouter(prefix="/tasks", tags=["tasks"])


# PUBLIC_INTERFACE
@router.get("/", response_model=list[schemas.Task])
def list_tasks(skip: int = 0, limit: int = 100, db_: Session = Depends(db.get_db)):
    """List all tasks."""
    return db_.query(models.Task).offset(skip).limit(limit).all()


@router.post("/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db_: Session = Depends(db.get_db)):
    """Create a new task."""
    new_task = models.Task(
        title=task.title,
        description=task.description,
        assigned_to_id=task.assigned_to_id,
        due_date=task.due_date,
    )
    db_.add(new_task)
    db_.commit()
    db_.refresh(new_task)
    return new_task
