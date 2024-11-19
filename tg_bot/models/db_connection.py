from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config
DATABASE_URL = Config.DATABASE_URL
def get_db_session():
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    return Session()