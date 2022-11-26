from sqlalchemy.orm import Session
from models import User

def db_register_user(db:Session, name, password):
    db_item = User(name=name, password=password)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item