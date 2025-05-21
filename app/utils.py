from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_env(key: str) -> str:
    value = os.getenv(key)
    if value is None:
        raise EnvironmentError(f"Missing environment variable: {key}")
    return value


def hash_this(password: str) -> str:
    return pwd_context.hash(password)


def verify_passwords(string_password, hashed_password):
    return pwd_context.verify(string_password, hashed_password)
