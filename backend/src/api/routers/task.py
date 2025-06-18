"""
Router for Task API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas, models, db, auth


router = APIRouter(prefix="/tasks", tags=["tasks"])


# PUBLIC_INTERFACE
@router.get("/", response_model=list[schemas.Task])
def list_tasks(
    skip: int = 0,
    limit: int = 100,
    db_: Session = Depends(db.get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """List all tasks (protected)."""
    return db_.query(models.Task).offset(skip).limit(limit).all()


@router.post("/", response_model=schemas.Task)
def create_task(
    task: schemas.TaskCreate,
    db_: Session = Depends(db.get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Create a new task (protected)."""
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


@router.get("/{task_id}", response_model=schemas.Task)
def get_task(
    task_id: int,
    db_: Session = Depends(db.get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Get task by id (protected)."""
    task = db_.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
