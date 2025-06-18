"""
Router for Dashboard API endpoints.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import db, models


router = APIRouter(prefix="/dashboard", tags=["dashboard"])


# PUBLIC_INTERFACE
@router.get("/summary")
def summary(db_: Session = Depends(db.get_db)):
    """
    Returns a minimal MVP dashboard summary:
    - count of users, roles, tasks, timesheets, leaves, open tasks, pending leaves
    """
    num_users = db_.query(models.User).count()
    num_roles = db_.query(models.Role).count()
    num_tasks = db_.query(models.Task).count()
    num_open_tasks = (
        db_.query(models.Task)
        .filter(models.Task.status != "completed")
        .count()
    )
    num_timesheets = db_.query(models.TimesheetEntry).count()
    num_leaves = db_.query(models.LeaveRequest).count()
    num_pending_leaves = (
        db_.query(models.LeaveRequest)
        .filter(models.LeaveRequest.status == "pending")
        .count()
    )
    return {
        "num_users": num_users,
        "num_roles": num_roles,
        "num_tasks": num_tasks,
        "num_open_tasks": num_open_tasks,
        "num_timesheets": num_timesheets,
        "num_leaves": num_leaves,
        "num_pending_leaves": num_pending_leaves,
    }
