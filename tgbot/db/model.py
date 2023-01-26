from sqlalchemy import Column, VARCHAR, INTEGER, DATE
from .base import BaseModel
import datetime


class Info(BaseModel):
    __tablename__ = 'info'

    id = Column(INTEGER(), primary_key=True, autoincrement=True)
    name = Column(VARCHAR(100), nullable=False)
    surname = Column(VARCHAR(100), nullable=False)
    job = Column(VARCHAR(500), nullable=False)
    number = Column(VARCHAR(15), nullable=False, unique=True)
    date = Column(DATE, default=datetime.date.today())

    def __str__(self) -> str:
        return f'<User:{self.name}'
