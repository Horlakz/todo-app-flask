from datetime import datetime
from dataclasses import dataclass
from sqlalchemy.orm import Mapped

from config.db import db

from .base import BaseModel
from .user import User


@dataclass
class Todo(BaseModel):
    __tablename__ = "todos"

    id: str
    title: str
    completed: bool
    created_at: datetime
    updated_at: datetime
    # user: Mapped[User]

    title = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Uuid, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", backref=db.backref("todos", lazy=True))

    def __repr__(self):
        return f"<Todo {self.title} user={self.user.email}>"
