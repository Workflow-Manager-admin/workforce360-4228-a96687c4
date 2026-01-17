from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import engine, Base
from .routers import (
    user_role,
    task,
    timesheet,
    leave,
    dashboard,
)
from .routers import auth as auth_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DB tables (for demo: auto-create; in prod use migrations)
Base.metadata.create_all(bind=engine)

# Include API routers
app.include_router(auth_router.router)
app.include_router(user_role.router)
app.include_router(task.router)
app.include_router(timesheet.router)
app.include_router(leave.router)
app.include_router(dashboard.router)


# PUBLIC_INTERFACE
@app.get("/")
def health_check():
    """Simple health check endpoint."""
    return {"message": "Healthy"}
