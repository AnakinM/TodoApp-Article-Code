from fastapi import FastAPI
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, MetaData
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import relationship, declared_attr

app = FastAPI()
SQLALCHEMY_DATABASE_URL = "sqlite:///db.sqlite"
meta = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_`%(constraint_name)s`",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
      })


@as_declarative(metadata=meta)
class Base(object):
    @declared_attr
    def __tablename__(cls):
        return f"{cls.__name__.lower()}s"
    id = Column(Integer, primary_key=True)


class Task(Base):
    note = Column(String)
    deadline = Column(DateTime)
    is_completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="tasks")


class User(Base):
    username = Column(String(20))
    email = Column(String(200))
    password = Column(String(200))
    tasks = relationship("Task", back_populates="user")


@app.get("/")
async def root():
    return {"message": "Hello World"}
