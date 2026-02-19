import enum
from datetime import datetime

from sqlalchemy import (

    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)

from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base




class UserRole(str, enum.Enum):
    admin = "admin"
    user = "user"
    manager = "manager"


class TaskStatus(str, enum.Enum):
    backlog = "backlog"
    in_progress = "in_progress"
    done = "done"


class ProjectStatus(str, enum.Enum):
    active = "active"
    completed = "completed"
    archived = "archived"


class PriorityLevel(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class ComplexityLevel(str, enum.Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"




class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    username: Mapped[str] = mapped_column(String(30),unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(30), nullable=False)

    role: Mapped[UserRole] = mapped_column(
        SAEnum(UserRole, name="user_role"),
        nullable=False,
        server_default= 'user'
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # relationships


    user_project: Mapped[list["UserProject"]] = relationship(
        back_populates="user",
        cascade ="all, delete-orphan",
    )

    user_task: Mapped[list["UserTask"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )



class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    status: Mapped[ProjectStatus] = mapped_column(
        SAEnum(ProjectStatus, name="project_status"),
        nullable=False,
        server_default= "active"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    deadline: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    performer_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)

    # relationships

    user_project: Mapped[list["UserProject"]] = relationship(
        back_populates="project",
        cascade ="all, delete-orphan",
    )

    task: Mapped[list["Task"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
    )


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    status: Mapped[TaskStatus] = mapped_column(
        SAEnum(TaskStatus, name="task_status"),
        nullable=False,
        server_default= "backlog"
    )
    priority: Mapped[PriorityLevel] = mapped_column(
        SAEnum(PriorityLevel, name="priority_level"),
        nullable=False,
        server_default= "medium"
    )
    complexity: Mapped[ComplexityLevel] = mapped_column(
        SAEnum(ComplexityLevel, name="complexity_level"),
        nullable=False,
        server_default= "medium"
    )

    deadline: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    performer_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)

    # relationships

    user_project: Mapped[list["UserProject"]] = relationship(
    back_populates="task",
    cascade="all, delete-orphan",
    )


class UserProject(Base):
    __tablename__ = "user_projects"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), primary_key=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )


    # relationships

    user: Mapped[list["User"]] = relationship(
        back_populates="user_project",
        cascade="all, delete-orphan",
    )

    project: Mapped[list["Project"]] = relationship(
        back_populates="user_project",
        cascade="all, delete-orphan",
    )
    user_task: Mapped[list["UserTask"]] = relationship(
        back_populates="user_project",
        cascade="all, delete-orphan",
    )



class UserTask(Base):
    __tablename__ = "user_tasks"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), primary_key=True)

    # у тебя в схеме есть project_id — оставляю.
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    # relationships

    user: Mapped[list["User"]] = relationship(
        back_populates="user_task",
        cascade="all, delete-orphan",
    )

    task: Mapped[list["Task"]] = relationship(
        back_populates="user_task",
        cascade="all, delete-orphan",
    )
    user_project: Mapped[list["UserProject"]] = relationship(
        back_populates="user_task",
        cascade="all, delete-orphan",
    )