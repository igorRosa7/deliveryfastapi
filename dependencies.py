from models import db
from sqlalchemy.orm import sessionmaker, Session

def get_session():
    Session = sessionmaker(bind=db)
    session = Session()
    return session