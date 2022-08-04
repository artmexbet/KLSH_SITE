from sqlalchemy import Column, String, Integer, ForeignKey, orm
from .db_session import SqlAlchemyBase


class Teams(SqlAlchemyBase):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    users = orm.relation("User", back_populates="team")
