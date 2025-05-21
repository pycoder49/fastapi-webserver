from jose import JWTError, jwt
from dotenv import load_dotenv
from .utils import verify_env


# SECRET_KEY
# Algorithm to use: hs256
# expiration time of the toke

SECRET_KEY = verify_env("SECRET_KEY")
ALGORITHM = verify_env("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = verify_env("ACCESS_TOKEN_EXPIRE_MINUTES")
