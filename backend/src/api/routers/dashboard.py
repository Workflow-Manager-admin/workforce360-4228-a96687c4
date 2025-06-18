"""
Router for Dashboard API endpoints.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


# PUBLIC_INTERFACE
@router.get("/summary")
def summary():
    """Returns a placeholder team summary."""
    return {"message": "Dashboard summary endpoint (to be implemented)"}
