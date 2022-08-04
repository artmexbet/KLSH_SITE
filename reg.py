from data import db_session
from data.users import User


db_session.global_init("db/klsh_db.db")
sess = db_session.create_session()
user = User()
user.name = "Артём Майдуров"
user.year = 10
user.login = "artmexbet"
user.set_password("1234")
user.team_id = 1
user.role_id = 3
sess.add(user)
sess.commit()
