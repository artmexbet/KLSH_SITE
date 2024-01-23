from sqlalchemy import Column, String, Integer, ForeignKey, orm
from .db_session import SqlAlchemyBase


class Competitions(SqlAlchemyBase):
    __tablename__ = "competitions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    achievements = orm.relationship("Achievements", back_populates="competition", cascade="all, delete")
