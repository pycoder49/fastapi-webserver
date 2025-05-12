from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL

from dotenv import load_dotenv
import os

load_dotenv()


def verify_env(key: str) -> str:
    value = os.getenv(key)
    if value is None:
        raise EnvironmentError(f"Missing environment variable: {key}")
    return value


url = URL.create(
    drivername="postgresql",
    username="postgres",
    password=verify_env("PASSWORD"),
    host="localhost",
    database="fastapi",
    port=5432
)

engine = create_engine(url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
