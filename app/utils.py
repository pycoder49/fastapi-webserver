from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_this(password: str) -> str:
    return pwd_context.hash(password)


def verify_passwords(string_password, hashed_password):
    return pwd_context.verify(string_password, hashed_password)
