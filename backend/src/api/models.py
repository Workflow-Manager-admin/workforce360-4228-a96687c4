"""
SQLAlchemy database models for WorkForce360 core resources.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
import enum
import datetime

from .db import Base


class UserRoleEnum(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    employee = "employee"


# User and Role


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, index=True, nullable=False)
    full_name = Column(String(128), nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)
    is_active = Column(Integer, default=1)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    role = relationship("Role", back_populates="users")
    timesheet_entries = relationship("TimesheetEntry", back_populates="user")
    leave_requests = relationship("LeaveRequest", back_populates="user")


# Task


class TaskStatusEnum(str, enum.Enum):
    open = "open"
    in_progress = "in_progress"
    completed = "completed"
    archived = "archived"


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(128), nullable=False)
    description = Column(Text, nullable=True)
    assigned_to_id = Column(Integer, ForeignKey('users.id'))
    assigned_to = relationship("User", foreign_keys=[assigned_to_id])
    status = Column(Enum(TaskStatusEnum), default=TaskStatusEnum.open)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    due_date = Column(DateTime, nullable=True)


# Timesheet


class TimesheetEntry(Base):
    __tablename__ = "timesheet_entries"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="timesheet_entries")
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=True)
    task = relationship("Task")
    date = Column(DateTime, default=datetime.date.today)
    hours = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


# Leave


class LeaveStatusEnum(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    cancelled = "cancelled"


class LeaveRequest(Base):
    __tablename__ = "leave_requests"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="leave_requests")
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    reason = Column(Text, nullable=True)
    status = Column(Enum(LeaveStatusEnum), default=LeaveStatusEnum.pending)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
