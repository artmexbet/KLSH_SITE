from sqlalchemy import Column, String, Integer, ForeignKey, orm
from .db_session import SqlAlchemyBase
from .punishments import Punishments
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    login = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    role = orm.relationship('Roles')
    team = orm.relationship('Teams')
    punishments = orm.relationship("Punishments", back_populates="student", cascade="all, delete")
    achievements = orm.relationship("Achievements", back_populates="student", cascade="all, delete")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
