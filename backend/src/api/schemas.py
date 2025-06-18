"""
Pydantic schemas for WorkForce360 resources: User, Role, Task, TimesheetEntry, LeaveRequest.
"""

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, date
import enum


class UserRoleEnum(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    employee = "employee"


class TaskStatusEnum(str, enum.Enum):
    open = "open"
    in_progress = "in_progress"
    completed = "completed"
    archived = "archived"


class LeaveStatusEnum(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    cancelled = "cancelled"


# Role


class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None


class RoleCreate(RoleBase):
    pass


class Role(RoleBase):
    id: int

    class Config:
        from_attributes = True


# User


class UserBase(BaseModel):
    username: str
    full_name: str
    email: EmailStr
    role_id: int


class UserRegister(BaseModel):
    username: str
    full_name: str
    email: EmailStr
    password: str
    role_id: Optional[int] = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True


# JWT Token


class Token(BaseModel):
    access_token: str
    token_type: str


# Task


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    assigned_to_id: Optional[int] = None


class Task(TaskBase):
    id: int
    assigned_to_id: Optional[int]
    status: TaskStatusEnum
    created_at: datetime

    class Config:
        from_attributes = True


# Timesheet


class TimesheetEntryBase(BaseModel):
    date: date
    hours: int
    description: Optional[str] = None
    task_id: Optional[int] = None


class TimesheetEntryCreate(TimesheetEntryBase):
    pass


class TimesheetEntry(TimesheetEntryBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Leave


class LeaveRequestBase(BaseModel):
    start_date: date
    end_date: date
    reason: Optional[str]
    status: LeaveStatusEnum = LeaveStatusEnum.pending


class LeaveRequestCreate(LeaveRequestBase):
    pass


class LeaveRequest(LeaveRequestBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
