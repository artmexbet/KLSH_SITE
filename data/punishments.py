from sqlalchemy import Column, String, Integer, ForeignKey, orm
from .db_session import SqlAlchemyBase


class Punishments(SqlAlchemyBase):
    __tablename__ = "punishments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    reason = Column(String, nullable=False)
    punishment = Column(String, nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    student = orm.relation('User')
