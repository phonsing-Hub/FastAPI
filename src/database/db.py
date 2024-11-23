from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine
from typing import Annotated
from dotenv import load_dotenv
import os
load_dotenv()
# สร้างการเชื่อมต่อกับฐานข้อมูล PostgreSQL
DATABASE_URL = os.getenv('DB_URL')
engine = create_engine(DATABASE_URL)
 

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
