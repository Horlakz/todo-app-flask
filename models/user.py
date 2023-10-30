from dataclasses import dataclass

from .base import BaseModel
from config.db import db


@dataclass
class User(BaseModel):
    __tablename__ = "users"

    id: str
    fullname: str
    email: str
    username: str
    created_at: str
    updated_at: str

    fullname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<User {self.email}>"
