from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from .config import settings

# for raw SWL
# from psycopg2.extras import RealDictCursor
# import psycopg2
# import time
# from . import utils


url = URL.create(
    drivername="postgresql",
    username=settings.database_username,
    password=settings.database_password,
    host=settings.database_hostname,
    database=settings.database_name,
    port=settings.database_port
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


# If you want to use raw SQL in python:
# while True:
#     try:
#         connection = psycopg2.connect(
#             host='localhost',
#             database='fastapi',
#             user='postgres',
#             password=utils.verify_env("PASSWORD"),
#             cursor_factory=RealDictCursor)
#         cursor = connection.cursor()
#         print("Database connection successful")
#         break
#     except Exception as error:
#         print("Database connection failed")
#         print("Error: ", error)
#         time.sleep(2)



