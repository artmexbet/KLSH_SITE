from sqlalchemy import Column, String, Integer, ForeignKey, orm
from .db_session import SqlAlchemyBase


class Achievements(SqlAlchemyBase):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, autoincrement=True)
    competition_id = Column(Integer, ForeignKey("competitions.id"), nullable=False)
    place = Column(Integer)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    competition = orm.relationship('Competitions')
    student = orm.relationship('User')
