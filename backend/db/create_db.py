from sqlalchemy import create_engine, MetaData
from src.models import Base
import time

DATABASE_URL = "mysql+mysqlconnector://username:password@db/image_db"

engine = create_engine(DATABASE_URL)
metadata = MetaData()

def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()
