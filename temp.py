from data import db_session
from data.teams import Teams

db_session.global_init("db/klsh_db.db")
sess = db_session.create_session()
a = sess.query(Teams).get(1).users
for i in a:
    print(i.name)
