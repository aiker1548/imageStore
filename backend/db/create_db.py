from sqlalchemy import create_engine, MetaData
from src.models import Base
from dotenv import load_dotenv
import os

load_dotenv()


DATABASE_URL = f"mysql+mysqlconnector://username:password@{os.getenv("DB_URL")}/image_db"

engine = create_engine(DATABASE_URL)
metadata = MetaData()

def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()
