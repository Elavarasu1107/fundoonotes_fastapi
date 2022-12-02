from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    create_engine,
    or_,
    select,
)
from sqlalchemy.orm import Session, declarative_base, relationship

from settings import settings

Base = declarative_base()
engine = create_engine(settings.database_url)
Base.metadata.create_all(engine)
session = Session(engine)


class Manager:
    def __init__(self) -> None:
        self.model = None
        # self.session = Session(engine)


    def create(self, **payload):
        instance = self.model(**payload)
        session.add(instance)
        session.commit()
        session.refresh(instance)
        return instance

    def add(self, instance):
        session.add(instance)
        session.commit()
        session.refresh(instance)

    def bulk_create(self, *instances):
        session.add_all(*instances)
        session.commit()

    def update(self, **payload):
        instance = self.get(id=payload.get("id"))
        for k, v in payload.items():
            setattr(instance, k, v)
        session.commit()
        session.refresh(instance)
        return instance

    def delete(self, **payload):
        instance = self.get(id=payload.get("id"))
        session.delete(instance)
        session.commit()

    def get(self, **payload):
        instance = session.query(self.model).filter_by(**payload).one()
        return instance

    def get_or_none(self, **payload):
        instance = session.query(self.model).filter_by(**payload).one_or_none()
        return instance

    def filter(self, **payload):
        instance_list = session.query(self.model).filter_by(**payload).all()
        return instance_list

    def all(self):
        instance_list = session.query(self.model).all()
        return instance_list

    def m2m_filter(self, **payload):
        instance_list = session.query(self.model).filter_by(or_(**payload)).all()
        return instance_list

    def save(self):
        session.commit()

    def __set_name__(self, owner, name):
        self.model = owner


class User(Base):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, index=True)
    username = Column(String(250), unique=True)
    password = Column(String(250))
    first_name = Column(String(150))
    last_name = Column(String(150))
    email = Column(String(150))
    phone = Column(BigInteger)
    location = Column(String(150))
    is_superuser = Column(Boolean, default=False)
    note = relationship("Notes", back_populates="user")
    notes = relationship("Notes", secondary="collaborator")
    objects = Manager()

    def __repr__(self):
        return f"User(id={self.id!r})"

    
    def to_dict(self):
        return {"id": self.id, "username": self.username, "first_name": self.first_name, "last_name": self.last_name,
                "email": self.email, "phone": self.phone, "location": self.location}


class Notes(Base):
    __tablename__ = "notes"

    id = Column(BigInteger, primary_key=True, index=True)
    title = Column(String(150))
    description = Column(String(150))
    user_id = Column(BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="notes")
    users = relationship("User", secondary="collaborator", overlaps='notes')
    objects = Manager()

    def __repr__(self):
        return f"User(id={self.id!r})"

    
    def to_dict(self):
        return {"id": self.id, "title": self.title, "description": self.description, "user_id": self.user_id}


class Collaborator(Base):
    __tablename__ = "collaborator"

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    note_id = Column(BigInteger, ForeignKey("notes.id", ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return f"User(id={self.id!r})"
